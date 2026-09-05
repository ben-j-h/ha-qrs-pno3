"""Diagnostics for QRS PNO3."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from . import PnoConfigEntry

_REDACT = {"mac", "wmac", "wip", "gw", "wgw", "dns", "wdns", "wcast", "wmask", "dealerInformation"}


def _scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: ("**REDACTED**" if k in _REDACT else _scrub(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [_scrub(v) for v in value]
    return value


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: PnoConfigEntry
) -> dict[str, Any]:
    rt = entry.runtime_data
    data = rt.coordinator.data
    return {
        "options": dict(entry.options),
        "library_stats": await rt.library.async_stats(),
        "playback": _scrub(data.playback if data else {}),
        "params_sample": {
            k: rt.coordinator.param(k) for k in (31, 47, 10000, 10001, 10002, 10003, 85)
        },
        "resolved_track": (
            {
                "music_id": data.track.music_id,
                "artist": data.track.artist,
                "title": data.track.title,
                "album": data.track.album,
            }
            if data and data.track
            else None
        ),
    }
