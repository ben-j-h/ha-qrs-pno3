"""Polling coordinator for the QRS PNO3."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import PnoApiClient, PnoConnectionError
from .const import (
    DEFAULT_IDLE_INTERVAL,
    DEFAULT_PARAMS_INTERVAL,
    DEFAULT_PLAYING_INTERVAL,
    DOMAIN,
    OPT_IDLE_INTERVAL,
    OPT_PARAMS_INTERVAL,
    OPT_PLAYING_INTERVAL,
    STATE_PAUSED,
    STATE_PLAYING,
)
from .library import PnoLibrary, Track

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class PnoData:
    """Everything the entities render from one poll cycle."""

    playback: dict[str, Any]
    params: dict[int, Any]
    track: Track | None
    updated_at: datetime
    library_stats: dict[str, Any] = field(default_factory=dict)

    # convenience -----------------------------------------------------
    @property
    def player_state(self) -> int:
        return int(self.playback.get("currentPlayerState", 0) or 0)

    @property
    def is_playing(self) -> bool:
        return self.player_state == STATE_PLAYING

    @property
    def is_paused(self) -> bool:
        return self.player_state == STATE_PAUSED

    @property
    def power_on(self) -> bool:
        return bool(self.playback.get("currentPowerOn"))


class PnoCoordinator(DataUpdateCoordinator[PnoData]):
    """Owns the API client + library and drives adaptive polling."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: PnoApiClient,
        library: PnoLibrary,
    ) -> None:
        self.api = api
        self.library = library
        self.entry = entry
        self._sys_state = "0"
        self._sys_settings = "0"
        self._params: dict[int, Any] = {}
        self._params_ts = 0.0
        self._last_lib_version: Any = None
        self._last_tag_version: Any = None
        self._syncing = False
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=self._opt(OPT_IDLE_INTERVAL, DEFAULT_IDLE_INTERVAL)),
        )

    # -- options ----------------------------------------------------
    def _opt(self, key: str, default: int) -> int:
        try:
            return int(self.entry.options.get(key, default))
        except (TypeError, ValueError):
            return default

    @property
    def _params_interval(self) -> int:
        return self._opt(OPT_PARAMS_INTERVAL, DEFAULT_PARAMS_INTERVAL)

    # -- polling --------------------------------------------------
    async def _async_update_data(self) -> PnoData:
        try:
            (
                playback,
                deltas,
                self._sys_state,
                self._sys_settings,
            ) = await self.api.async_quick_state(self._sys_state, self._sys_settings)
        except PnoConnectionError as err:
            raise UpdateFailed(str(err)) from err

        self._params.update(deltas)

        # master volume et al. are not in the quick delta stream - refresh the
        # full param table on a slow cadence (and once on first run).
        now = time.monotonic()
        if self._params_interval and (now - self._params_ts) >= self._params_interval:
            try:
                self._params.update(await self.api.async_all_params())
            except PnoConnectionError as err:  # non-fatal
                _LOGGER.debug("param refresh failed: %s", err)
            else:
                self._params_ts = now

        # kick a library sync if the controller bumped its versions
        lib_v = playback.get("libraryVersion")
        tag_v = playback.get("tagVersion")
        if (lib_v, tag_v) != (self._last_lib_version, self._last_tag_version):
            self._last_lib_version, self._last_tag_version = lib_v, tag_v
            self._schedule_library_sync(lib_v, tag_v)

        track: Track | None = None
        music_id = playback.get("currentMusicId")
        if music_id is not None:
            track = await self.library.async_get_track(int(music_id))

        stats = self.data.library_stats if self.data else {}
        if not stats:
            try:
                stats = await self.library.async_stats()
            except Exception as err:
                _LOGGER.debug("library stats unavailable: %s", err)
                stats = {}

        # adaptive interval
        if int(playback.get("currentPlayerState", 0) or 0) in (STATE_PLAYING, STATE_PAUSED):
            interval = self._opt(OPT_PLAYING_INTERVAL, DEFAULT_PLAYING_INTERVAL)
        elif playback.get("currentPowerOn"):
            interval = max(5, self._opt(OPT_IDLE_INTERVAL, DEFAULT_IDLE_INTERVAL) // 3)
        else:
            interval = self._opt(OPT_IDLE_INTERVAL, DEFAULT_IDLE_INTERVAL)
        self.update_interval = timedelta(seconds=interval)

        return PnoData(
            playback=playback,
            params=dict(self._params),
            track=track,
            updated_at=dt_util.utcnow(),
            library_stats=stats,
        )

    # -- library sync ------------------------------------------
    def _schedule_library_sync(self, lib_v: Any, tag_v: Any) -> None:
        if self._syncing:
            return
        self._syncing = True

        async def _run() -> None:
            try:
                await self.library.async_sync_if_changed(lib_v, tag_v)
                stats = await self.library.async_stats()
                if self.data:
                    self.data.library_stats = stats
            except Exception:
                _LOGGER.exception("PNO3 library sync failed")
            finally:
                self._syncing = False

        self.entry.async_create_background_task(self.hass, _run(), "qrs_pno3 library sync")

    async def async_refresh_library(self) -> dict[str, Any]:
        """Force a full rebuild - used by the ``refresh_library`` service/button."""
        self._syncing = True
        try:
            stats = await self.library.async_rebuild()
        finally:
            self._syncing = False
        if self.data:
            self.data.library_stats = stats
        await self.async_request_refresh()
        return stats

    # -- helpers for entities --------------------------------
    def param(self, param_id: int, default: Any = None) -> Any:
        return self._params.get(param_id, default)

    def set_param_cache(self, param_id: int, value: Any) -> None:
        """Optimistically record a value we just wrote, until the next refresh."""
        self._params[param_id] = value
        if self.data:
            self.data.params[param_id] = value
