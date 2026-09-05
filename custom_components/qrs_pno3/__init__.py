"""The QRS PNO3 Player Piano integration."""

from __future__ import annotations

import contextlib
import logging
import os
from dataclasses import dataclass

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PnoApiClient, PnoError
from .const import (
    ATTR_APPLY_CHECKSUM,
    ATTR_COMMAND,
    ATTR_ENTRY_ID,
    ATTR_MUSIC_ID,
    ATTR_QUERY,
    ATTR_VALUE,
    CONF_HOST,
    DOMAIN,
    PARAM_TEMPO,
    PARAM_TRANSPOSE,
    SERVICE_CLEAR_FAULTS,
    SERVICE_PLAY_SONG,
    SERVICE_REFRESH_LIBRARY,
    SERVICE_SEND_COMMAND,
    SERVICE_SET_TEMPO,
    SERVICE_SET_TRANSPOSE,
    STORAGE_SUBDIR,
    TEMPO_MAX,
    TEMPO_MIN,
    TRANSPOSE_MAX,
    TRANSPOSE_MIN,
)
from .coordinator import PnoCoordinator
from .library import PnoLibrary

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.MEDIA_PLAYER,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BUTTON,
    Platform.NUMBER,
]


@dataclass(slots=True)
class PnoRuntimeData:
    """Stored on ``entry.runtime_data``."""

    api: PnoApiClient
    coordinator: PnoCoordinator
    library: PnoLibrary


type PnoConfigEntry = ConfigEntry[PnoRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: PnoConfigEntry) -> bool:
    """Set up QRS PNO3 from a config entry."""
    session = async_get_clientsession(hass)
    api = PnoApiClient(entry.data[CONF_HOST], session)

    db_dir = hass.config.path(".storage", STORAGE_SUBDIR)
    await hass.async_add_executor_job(os.makedirs, db_dir, True)
    library = PnoLibrary(hass, api, os.path.join(db_dir, f"{entry.entry_id}.db"))
    await library.async_setup()

    coordinator = PnoCoordinator(hass, entry, api, library)
    await coordinator.async_config_entry_first_refresh()

    # The coordinator kicks a full library build on first poll (it sees the
    # library/tag version change from "unknown"), so nothing else to do here.
    entry.runtime_data = PnoRuntimeData(api, coordinator, library)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_reload_on_options))
    _async_register_services(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PnoConfigEntry) -> bool:
    """Unload a config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not hass.config_entries.async_loaded_entries(DOMAIN):
        for service in (
            SERVICE_REFRESH_LIBRARY,
            SERVICE_PLAY_SONG,
            SERVICE_SEND_COMMAND,
            SERVICE_SET_TEMPO,
            SERVICE_SET_TRANSPOSE,
            SERVICE_CLEAR_FAULTS,
        ):
            hass.services.async_remove(DOMAIN, service)
    return unloaded


async def _async_reload_on_options(hass: HomeAssistant, entry: PnoConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_entry(hass: HomeAssistant, entry: PnoConfigEntry) -> None:
    """Delete the per-entry library cache file when the integration is removed."""
    db_path = hass.config.path(".storage", STORAGE_SUBDIR, f"{entry.entry_id}.db")

    def _cleanup() -> None:
        for suffix in ("", "-wal", "-shm"):
            with contextlib.suppress(FileNotFoundError):
                os.remove(db_path + suffix)

    await hass.async_add_executor_job(_cleanup)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
_ENTRY_SELECTOR = {vol.Optional(ATTR_ENTRY_ID): vol.All(cv.ensure_list, [cv.string])}


@callback
def _async_register_services(hass: HomeAssistant) -> None:
    if hass.services.has_service(DOMAIN, SERVICE_REFRESH_LIBRARY):
        return

    def _targets(call: ServiceCall) -> list[PnoRuntimeData]:
        wanted = call.data.get(ATTR_ENTRY_ID)
        entries = hass.config_entries.async_loaded_entries(DOMAIN)
        if wanted:
            entries = [e for e in entries if e.entry_id in wanted]
        if not entries:
            raise ServiceValidationError("No loaded QRS PNO3 config entries matched")
        return [e.runtime_data for e in entries]

    async def _refresh_library(call: ServiceCall) -> None:
        for rt in _targets(call):
            await rt.coordinator.async_refresh_library()

    async def _play_song(call: ServiceCall) -> None:
        music_id = call.data.get(ATTR_MUSIC_ID)
        query = call.data.get(ATTR_QUERY)
        for rt in _targets(call):
            track = None
            if music_id is not None:
                track = await rt.library.async_get_track(int(music_id))
            elif query:
                hits = await rt.library.async_search(query, limit=1)
                track = hits[0] if hits else None
            if track is None:
                raise ServiceValidationError(
                    f"No song found for music_id={music_id!r} query={query!r}"
                )
            try:
                await rt.api.async_play_song(track.library_id, track.music_id)
            except PnoError as err:
                raise HomeAssistantError(str(err)) from err
            await rt.coordinator.async_request_refresh()

    async def _send_command(call: ServiceCall) -> None:
        raw = call.data[ATTR_COMMAND]
        apply = call.data.get(ATTR_APPLY_CHECKSUM, True)
        for rt in _targets(call):
            try:
                await rt.api.async_send_command(raw, apply_checksum=apply)
            except PnoError as err:
                raise HomeAssistantError(str(err)) from err
            await rt.coordinator.async_request_refresh()

    def _make_param_setter(param_id: int):
        async def _setter(call: ServiceCall) -> None:
            value = call.data[ATTR_VALUE]
            for rt in _targets(call):
                try:
                    await rt.api.async_set_param(param_id, value)
                except PnoError as err:
                    raise HomeAssistantError(str(err)) from err
                await rt.coordinator.async_request_refresh()

        return _setter

    async def _clear_faults(call: ServiceCall) -> None:
        for rt in _targets(call):
            await rt.api.async_clear_faults()
            await rt.coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN, SERVICE_REFRESH_LIBRARY, _refresh_library, schema=vol.Schema(_ENTRY_SELECTOR)
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_PLAY_SONG,
        _play_song,
        schema=vol.Schema(
            {
                **_ENTRY_SELECTOR,
                vol.Exclusive(ATTR_MUSIC_ID, "song"): cv.positive_int,
                vol.Exclusive(ATTR_QUERY, "song"): cv.string,
            }
        ),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_COMMAND,
        _send_command,
        schema=vol.Schema(
            {
                **_ENTRY_SELECTOR,
                vol.Required(ATTR_COMMAND): cv.string,
                vol.Optional(ATTR_APPLY_CHECKSUM, default=True): cv.boolean,
            }
        ),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_TEMPO,
        _make_param_setter(PARAM_TEMPO),
        schema=vol.Schema(
            {
                **_ENTRY_SELECTOR,
                vol.Required(ATTR_VALUE): vol.All(vol.Coerce(int), vol.Range(TEMPO_MIN, TEMPO_MAX)),
            }
        ),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_TRANSPOSE,
        _make_param_setter(PARAM_TRANSPOSE),
        schema=vol.Schema(
            {
                **_ENTRY_SELECTOR,
                vol.Required(ATTR_VALUE): vol.All(
                    vol.Coerce(int), vol.Range(TRANSPOSE_MIN, TRANSPOSE_MAX)
                ),
            }
        ),
    )
    hass.services.async_register(
        DOMAIN, SERVICE_CLEAR_FAULTS, _clear_faults, schema=vol.Schema(_ENTRY_SELECTOR)
    )
