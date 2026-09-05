"""Media player entity for the QRS PNO3 player piano."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.media_player import (
    BrowseMedia,
    MediaClass,
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
    RepeatMode,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import PnoConfigEntry
from .api import PnoError
from .const import (
    DEFAULT_TURN_OFF_STOPS,
    OPT_TURN_OFF_STOPS,
    PARAM_MASTER_VOLUME,
    STATE_PAUSED,
    STATE_PLAYING,
)
from .entity import PnoEntity

_LOGGER = logging.getLogger(__name__)

_REPEAT_TO_MODE = {RepeatMode.OFF: 0, RepeatMode.ONE: 1, RepeatMode.ALL: 2}
_MODE_TO_REPEAT = {0: RepeatMode.OFF, 1: RepeatMode.ONE, 2: RepeatMode.ALL}
_VOLUME_STEP = 0.05

_ROOT = "root"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PnoConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    async_add_entities([PnoMediaPlayer(entry.runtime_data.coordinator)])


class PnoMediaPlayer(PnoEntity, MediaPlayerEntity):
    """Control + now-playing for the piano."""

    _attr_name = None
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_media_content_type = MediaType.MUSIC
    _attr_supported_features = (
        MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.STOP
        | MediaPlayerEntityFeature.NEXT_TRACK
        | MediaPlayerEntityFeature.PREVIOUS_TRACK
        | MediaPlayerEntityFeature.SEEK
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.REPEAT_SET
        | MediaPlayerEntityFeature.SHUFFLE_SET
        | MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.PLAY_MEDIA
        | MediaPlayerEntityFeature.BROWSE_MEDIA
    )

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_media_player"
        self._muted_volume: float | None = None

    # -- state --------------------------------------------------
    @property
    def state(self) -> MediaPlayerState:
        ps = self.coordinator.data.player_state
        if ps == STATE_PLAYING:
            return MediaPlayerState.PLAYING
        if ps == STATE_PAUSED:
            return MediaPlayerState.PAUSED
        if self.coordinator.data.power_on:
            return MediaPlayerState.IDLE
        return MediaPlayerState.OFF

    @property
    def volume_level(self) -> float | None:
        raw = self.coordinator.param(PARAM_MASTER_VOLUME)
        if raw is None:
            return None
        try:
            return max(0.0, min(1.0, float(raw) / 100.0))
        except (TypeError, ValueError):
            return None

    @property
    def is_volume_muted(self) -> bool | None:
        if self._pb.get("mute_master"):
            return True
        return self._muted_volume is not None

    @property
    def media_duration(self) -> int | None:
        ms = self._pb.get("currentTrackDurationMs") or 0
        return int(ms // 1000) if ms and ms > 0 else None

    @property
    def media_position(self) -> int | None:
        ms = self._pb.get("currentTrackProgrssMs")
        if ms is None or ms < 0:
            return None
        return int(ms // 1000)

    @property
    def media_position_updated_at(self):
        return self.coordinator.data.updated_at

    @property
    def media_content_id(self) -> str | None:
        mid = self._pb.get("currentMusicId")
        return f"song:{mid}" if mid is not None else None

    @property
    def media_title(self) -> str | None:
        track = self.coordinator.data.track
        if track and track.title:
            return track.title
        return self._title_from_status()

    @property
    def media_artist(self) -> str | None:
        track = self.coordinator.data.track
        if track and track.artist:
            return track.artist
        return None

    @property
    def media_album_name(self) -> str | None:
        track = self.coordinator.data.track
        return track.album if track and track.album else None

    @property
    def media_playlist(self) -> str | None:
        return self._pb.get("playListName") or None

    @property
    def repeat(self) -> RepeatMode | None:
        return _MODE_TO_REPEAT.get(int(self._pb.get("repeat", 0) or 0))

    @property
    def shuffle(self) -> bool | None:
        return bool(self._pb.get("shuffle"))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        pb = self._pb
        track = self.coordinator.data.track
        attrs: dict[str, Any] = {
            "music_id": pb.get("currentMusicId"),
            "library_id": pb.get("currentLibraryId"),
            "file_path": pb.get("filePath"),
            "system_faults": pb.get("systemFaults"),
            "system_warnings": pb.get("systemWarnings"),
            "rail_power_on": pb.get("currentPowerOn"),
            "tempo": pb.get("tempo"),
            "transpose": pb.get("transpose"),
        }
        if track:
            attrs["genre"] = track.genre or None
            attrs["catalog"] = track.src.rsplit("/", 2)[-2] if "/" in track.src else None
        return attrs

    def _title_from_status(self) -> str | None:
        # fallback only - coordinator does not fetch getStatus, so this is rarely hit
        path = self._pb.get("filePath")
        return path.rsplit("/", 1)[-1] if path else None

    # -- commands ---------------------------------------------
    async def _do(self, coro) -> None:
        try:
            await coro
        except PnoError as err:
            raise HomeAssistantError(str(err)) from err
        await self.coordinator.async_request_refresh()

    async def async_media_play(self) -> None:
        await self._do(self.coordinator.api.async_play())

    async def async_media_pause(self) -> None:
        await self._do(self.coordinator.api.async_pause())

    async def async_media_stop(self) -> None:
        await self._do(self.coordinator.api.async_stop())

    async def async_media_seek(self, position: float) -> None:
        await self._do(self.coordinator.api.async_seek(int(position * 1000)))

    async def async_set_volume_level(self, volume: float) -> None:
        level = round(volume * 100)
        await self._do(self.coordinator.api.async_set_volume(level))
        self.coordinator.set_param_cache(PARAM_MASTER_VOLUME, level)  # optimistic

    async def async_volume_up(self) -> None:
        cur = self.volume_level or 0.0
        await self.async_set_volume_level(min(1.0, cur + _VOLUME_STEP))

    async def async_volume_down(self) -> None:
        cur = self.volume_level or 0.0
        await self.async_set_volume_level(max(0.0, cur - _VOLUME_STEP))

    async def async_mute_volume(self, mute: bool) -> None:
        if mute:
            self._muted_volume = self.volume_level
            await self.async_set_volume_level(0.0)
        else:
            restore = self._muted_volume if self._muted_volume is not None else 0.4
            self._muted_volume = None
            await self.async_set_volume_level(restore)

    async def async_set_repeat(self, repeat: RepeatMode) -> None:
        await self._do(self.coordinator.api.async_set_repeat(_REPEAT_TO_MODE.get(repeat, 0)))

    async def async_set_shuffle(self, shuffle: bool) -> None:
        await self._do(self.coordinator.api.async_set_shuffle(shuffle))

    async def async_turn_on(self) -> None:
        await self._do(self.coordinator.api.async_set_power(True))

    async def async_turn_off(self) -> None:
        stops = self.coordinator.entry.options.get(OPT_TURN_OFF_STOPS, DEFAULT_TURN_OFF_STOPS)
        if stops:
            await self.coordinator.api.async_stop()
        await self._do(self.coordinator.api.async_set_power(False))

    async def async_media_next_track(self) -> None:
        await self._advance(previous=False)

    async def async_media_previous_track(self) -> None:
        # position > 3s -> restart current (matches the controller's own "V")
        if (self._pb.get("currentTrackProgrssMs") or 0) > 3000:
            await self._do(self.coordinator.api.async_send_command("V"))
            return
        await self._advance(previous=True)

    async def _advance(self, *, previous: bool) -> None:
        pb = self._pb
        cur = pb.get("currentMusicId")
        if cur is None:
            return
        nxt: int | None = None
        list_id = pb.get("currentPlaylistId")
        if pb.get("currentPlaylistType") == 2 and isinstance(list_id, int):
            tracks = await self.coordinator.library.async_playlist_tracks(list_id)
            ids = [t.music_id for t in tracks]
            if cur in ids:
                i = ids.index(cur) + (-1 if previous else 1)
                if 0 <= i < len(ids):
                    nxt = ids[i]
        if nxt is None:
            nxt = await self.coordinator.library.async_next_music_id(int(cur), previous=previous)
        if nxt is None:
            return
        track = await self.coordinator.library.async_get_track(nxt)
        lib = track.library_id if track else pb.get("currentLibraryId", 1)
        await self._do(self.coordinator.api.async_play_song(int(lib), int(nxt)))

    async def async_play_media(self, media_type: str, media_id: str, **kwargs: Any) -> None:
        track = None
        lib = self._pb.get("currentLibraryId", 1)
        if media_id.startswith("song:"):
            track = await self.coordinator.library.async_get_track(int(media_id[5:]))
        elif media_id.startswith("playlist:"):
            list_id = int(media_id[9:])
            tracks = await self.coordinator.library.async_playlist_tracks(list_id)
            if not tracks:
                raise ServiceValidationError(f"Playlist {list_id} is empty or not cached")
            track = tracks[0]
        else:
            hits = await self.coordinator.library.async_search(media_id, limit=1)
            track = hits[0] if hits else None
        if track is None:
            raise ServiceValidationError(f"Nothing in the cache matched {media_id!r}")
        await self._do(
            self.coordinator.api.async_play_song(track.library_id or lib, track.music_id)
        )

    # -- browse ---------------------------------------------
    async def async_browse_media(
        self, media_content_type: str | None = None, media_content_id: str | None = None
    ) -> BrowseMedia:
        cid = media_content_id or _ROOT
        if cid == _ROOT:
            return self._browse_root()
        kind, _, value = cid.partition(":")
        if kind == "cat":
            return await self._browse_category(value)
        if kind in ("artist", "album", "genre"):
            tracks = await self.coordinator.library.async_by(kind, value)
            return self._browse_tracks(cid, value.title() if value else kind, tracks)
        if kind == "playlist":
            tracks = await self.coordinator.library.async_playlist_tracks(int(value))
            return self._browse_tracks(cid, f"Playlist {value}", tracks)
        raise ServiceValidationError(f"Unknown media id {cid!r}")

    def _browse_root(self) -> BrowseMedia:
        children = [
            BrowseMedia(
                title=title,
                media_class=MediaClass.DIRECTORY,
                media_content_type="",
                media_content_id=f"cat:{key}",
                can_play=False,
                can_expand=True,
            )
            for key, title in (
                ("playlists", "Playlists"),
                ("artist", "Artists"),
                ("album", "Albums"),
                ("genre", "Genres"),
            )
        ]
        return BrowseMedia(
            title=self.coordinator.entry.title,
            media_class=MediaClass.DIRECTORY,
            media_content_type="",
            media_content_id=_ROOT,
            can_play=False,
            can_expand=True,
            children=children,
        )

    async def _browse_category(self, key: str) -> BrowseMedia:
        if key == "playlists":
            pls = await self.coordinator.library.async_playlists()
            children = [
                BrowseMedia(
                    title=pl["name"],
                    media_class=MediaClass.PLAYLIST,
                    media_content_type=MediaType.PLAYLIST,
                    media_content_id=f"playlist:{pl['list_id']}",
                    can_play=True,
                    can_expand=True,
                )
                for pl in pls
            ]
        else:
            values = await self.coordinator.library.async_distinct(key)
            children = [
                BrowseMedia(
                    title=v,
                    media_class=MediaClass.DIRECTORY,
                    media_content_type="",
                    media_content_id=f"{key}:{v}",
                    can_play=False,
                    can_expand=True,
                )
                for v in values
            ]
        return BrowseMedia(
            title=key.title(),
            media_class=MediaClass.DIRECTORY,
            media_content_type="",
            media_content_id=f"cat:{key}",
            can_play=False,
            can_expand=True,
            children=children,
        )

    def _browse_tracks(self, cid: str, title: str, tracks) -> BrowseMedia:
        children = [
            BrowseMedia(
                title=t.display,
                media_class=MediaClass.MUSIC,
                media_content_type=MediaType.MUSIC,
                media_content_id=f"song:{t.music_id}",
                can_play=True,
                can_expand=False,
            )
            for t in tracks
        ]
        return BrowseMedia(
            title=title,
            media_class=MediaClass.DIRECTORY,
            media_content_type="",
            media_content_id=cid,
            can_play=bool(children),
            can_expand=True,
            children=children,
            children_media_class=MediaClass.MUSIC,
        )
