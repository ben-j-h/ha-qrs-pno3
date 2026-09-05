"""HTTP client for the QRS PNO3 / PNOmation III controller.

Everything the controller exposes is unauthenticated HTTP GET against
``http://<host>/php/*``.  Responses are JSON, XML, or JS-with-a-prefix.

See ``research/01-http-api-reference.md`` and ``research/06-live-test-results.md``
for how each endpoint was reverse engineered and verified.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any
from urllib.parse import quote

import aiohttp
from yarl import URL

_LOGGER = logging.getLogger(__name__)

_TIMEOUT = aiohttp.ClientTimeout(total=15)
_QUICK_TIMEOUT = aiohttp.ClientTimeout(total=10)


class PnoError(Exception):
    """Base error."""


class PnoConnectionError(PnoError):
    """Raised when the controller cannot be reached / replied nonsense."""


class PnoCommandError(PnoError):
    """Raised when the controller reported ``success=false`` for a command."""


def pno_checksum(command: str) -> str:
    """Encode a ``sendCommand`` payload.

    The controller expects each ``__``-separated sub-command to be prefixed with
    the decimal sum of the ASCII codes of every character that is not ``|``,
    followed by the sub-command (which is forced to start with ``|``).

    Verified live: ``"$|60000"`` -> ``"282|$|60000"``.
    """
    parts: list[str] = []
    for part in command.split("__"):
        total = sum(ord(ch) for ch in part if ch != "|")
        if not part.startswith("|"):
            part = "|" + part
        parts.append(f"{total}{part}")
    return "__".join(parts)


def _raw_decode(text: str, opener: str) -> Any:
    """Decode the first JSON value that starts at ``opener`` and ignore trailing junk.

    ``all_stream.php?js`` and ``tags.php`` both append non-JSON tails
    (bootstrap JS / PHP warnings); ``json.loads`` would choke on them.
    """
    try:
        start = text.index(opener)
    except ValueError as err:
        raise PnoConnectionError(f"no {opener!r} in response: {text[:120]!r}") from err
    try:
        value, _ = json.JSONDecoder().raw_decode(text, start)
    except json.JSONDecodeError as err:
        raise PnoConnectionError(f"bad JSON: {err} :: {text[:120]!r}") from err
    return value


class PnoApiClient:
    """Thin async wrapper around the controller's PHP endpoints."""

    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        self._host = host
        self._session = session

    @property
    def host(self) -> str:
        return self._host

    # -- low level ----------------------------------------------------------
    async def _text(self, path: str, *, timeout: aiohttp.ClientTimeout = _TIMEOUT) -> str:
        """GET ``/php/<path>`` and return the body text.

        ``path`` already contains its (pre-encoded) query string.  We build the
        URL by hand and pass it ``encoded=True`` so aiohttp does not re-encode
        the ``|`` / ``$`` in ``sendCommand`` payloads.
        """
        sep = "&" if "?" in path else "?"
        url = URL(
            f"http://{self._host}/php/{path}{sep}date={int(time.time() * 1000)}",
            encoded=True,
        )
        try:
            async with self._session.get(url, timeout=timeout) as resp:
                resp.raise_for_status()
                return await resp.text()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise PnoConnectionError(f"GET {path} failed: {err}") from err

    async def _command(self, query: str, *, json_variant: bool = True) -> dict[str, Any]:
        """Issue a control command and parse the JSON envelope.

        The controller frequently returns ``"success":false,"message":"Failed to
        Update!"`` even for calls that worked (notably ``getStatus``); callers
        that care pass ``expect_success`` handling themselves.
        """
        endpoint = "changePlaySettingsJSON.php" if json_variant else "changeSettingsJSON.php"
        text = await self._text(f"{endpoint}?{query}")
        try:
            return _raw_decode(text, "{")
        except PnoConnectionError:
            # XML fallback path or garbage - surface the raw text.
            _LOGGER.debug("non-JSON command reply for %s: %s", query, text[:200])
            return {"success": "true" in text.lower(), "_raw": text}

    # -- state ------------------------------------------------------------
    async def async_quick_state(
        self,
        system_state: str = "0",
        system_settings: str = "0",
        full_count: str = "0",
        demo_count: str = "0",
        temp_count: str = "0",
    ) -> tuple[dict[str, Any], dict[int, Any], str, str]:
        """Poll ``all_stream.php?quick=1``.

        Returns ``(playbackInformation, settings_deltas, system_state, system_settings)``.
        Pass the previous ``system_state`` / ``system_settings`` back in to get
        an incremental reply.
        """
        query = (
            f"all_stream.php?quick=1&settings={system_settings}&state={system_state}"
            f"&fullCount={full_count}&demoCount={demo_count}&tempCount={temp_count}"
        )
        text = await self._text(query, timeout=_QUICK_TIMEOUT)
        arr = _raw_decode(text, "[")
        if not isinstance(arr, list):
            raise PnoConnectionError(f"unexpected all_stream shape: {text[:120]!r}")

        deltas: dict[int, Any] = {}
        playback: dict[str, Any] | None = None
        new_state, new_settings = system_state, system_settings
        for elem in arr:
            if not isinstance(elem, dict):
                continue
            if elem.get("id") == -1:
                playback = elem.get("playbackInformation") or {}
                new_state = str(elem.get("system_state", new_state)).strip("'\"")
                new_settings = str(elem.get("system_settings", new_settings)).strip("'\"")
            elif "id" in elem and "val" in elem:
                deltas[int(elem["id"])] = elem["val"]

        if playback is None:
            raise PnoConnectionError("all_stream reply had no playbackInformation")
        return playback, deltas, new_state, new_settings

    async def async_network_info(self) -> dict[str, Any]:
        """One-shot full poll, returning ``playbackInformation.networkConnection``.

        Used only by the config flow to derive a stable unique id (MAC).
        """
        query = "all_stream.php?quick=0&settings=0&state=0&fullCount=0&demoCount=0&tempCount=0"
        text = await self._text(query)
        arr = _raw_decode(text, "[")
        for elem in arr if isinstance(arr, list) else []:
            if isinstance(elem, dict) and elem.get("id") == -1:
                pb = elem.get("playbackInformation") or {}
                return pb.get("networkConnection") or {}
        return {}

    async def async_all_params(self) -> dict[int, Any]:
        """Full controller parameter table from ``all_stream.php?js`` (``qrs.vals``).

        ~290 KB.  ``val`` holds the *current* value (verified: id 85 ``v=0/val=10``).
        Used sparingly to read things ``quick`` polling omits, e.g. master volume.
        """
        text = await self._text("all_stream.php?js")
        arr = _raw_decode(text, "[")
        out: dict[int, Any] = {}
        for elem in arr:
            if isinstance(elem, dict) and "id" in elem:
                try:
                    out[int(elem["id"])] = elem.get("val")
                except (TypeError, ValueError):
                    continue
        return out

    async def async_get_status(self) -> dict[str, Any]:
        """``getStatus`` - small JSON incl. human ``"Artist - Title (path)"``."""
        return await self._command("requestType=getStatus")

    # -- library feeds --------------------------------------------------
    async def async_music_stream(
        self, epoch: str = "0", epoch2: str = "0"
    ) -> tuple[list[dict[str, Any]], str, str]:
        """``music_stream.php`` - musicId <-> libraryId <-> file path, incremental.

        Returns ``(rows, next_epoch, next_epoch2)``.  ``rows`` items look like
        ``{"d":0,"lid":1,"id":2489,"src":".../801341/01.qrs"}`` (``d=1`` == removed).
        """
        text = await self._text(f"music_stream.php?epoch={epoch}&epoch2={epoch2}")
        arr = _raw_decode(text, "[")
        rows: list[dict[str, Any]] = []
        next_epoch, next_epoch2 = epoch, epoch2
        for elem in arr:
            if not isinstance(elem, dict):
                continue
            if "timeStamp" in elem:
                next_epoch = str(elem.get("timeStamp", epoch)).strip("'\"")
                next_epoch2 = str(elem.get("timeStampTemp", epoch2)).strip("'\"")
            elif "src" in elem:
                rows.append(elem)
        return rows, next_epoch, next_epoch2

    async def async_tags(self) -> dict[str, Any]:
        """``tags.php?epoch=0`` - title/artist/genre keyed by ``catalog -> track``.

        ``{"801341": {"alb": "...", "1": {"sng": "...", "art": "...", "gre": "..."}}}``
        """
        text = await self._text("tags.php?epoch=0")
        return _raw_decode(text, "{")

    async def async_playlists(self) -> list[dict[str, Any]]:
        """``playlist.php?function=list`` - local playlists (+ store promos)."""
        text = await self._text("playlist.php?function=list")
        arr = _raw_decode(text, "[")
        return [e for e in arr if isinstance(e, dict)]

    async def async_playlist_tracks(self, list_id: int) -> list[dict[str, Any]]:
        """``playlist.php?function=retrieve&id=<n>`` - ``[{"tid","lid","src"}, ...]``."""
        text = await self._text(f"playlist.php?function=retrieve&id={int(list_id)}")
        arr = _raw_decode(text, "[")
        return [e for e in arr if isinstance(e, dict) and "src" in e]

    # -- transport / control ------------------------------------------
    async def _play_command(self, query: str) -> None:
        reply = await self._command(query)
        # setPlayMode replies with a real success flag we can trust.
        if str(reply.get("success")).lower() == "false":
            raise PnoCommandError(f"{query} -> {reply}")

    async def async_play_song(self, library_id: int, music_id: int, restart: bool = True) -> None:
        await self._play_command(
            "requestType=setPlayMode&playSource=F&state=1"
            f"&libraryId={int(library_id)}&songId={int(music_id)}&restart={1 if restart else 0}"
        )

    async def async_play(self) -> None:
        await self._play_command("requestType=setPlayMode&state=1")

    async def async_pause(self) -> None:
        await self._play_command("requestType=setPlayMode&state=2")

    async def async_stop(self) -> None:
        await self._play_command("requestType=setPlayMode&state=0")

    async def async_seek(self, position_ms: int) -> None:
        await self.async_send_command(f"$|{max(0, int(position_ms))}")

    async def async_set_power(self, on: bool) -> None:
        await self._command(f"requestType=setPower&powerOn={1 if on else 0}")

    async def async_set_repeat(self, mode: int) -> None:
        await self._command(f"requestType=setRepeat&val={int(mode)}")

    async def async_set_shuffle(self, on: bool) -> None:
        await self._command(f"requestType=setShuffle&val={1 if on else 0}")

    async def async_clear_faults(self) -> None:
        await self._command("requestType=clrFaults")

    async def async_send_command(self, raw: str, *, apply_checksum: bool = True) -> dict[str, Any]:
        """Fire a raw pipe-language command through ``sendCommand``."""
        payload = pno_checksum(raw) if apply_checksum else raw
        return await self._command(f"requestType=sendCommand&msg={quote(payload, safe='')}")

    async def async_set_param(self, param: int, value: float, *, quick: bool = False) -> None:
        """Write a controller parameter via ``changeSettingsJSON.php``."""
        rt = "setQuickParam" if quick else "setParam"
        reply = await self._command(
            f"requestType={rt}&param={int(param)}&val={value}", json_variant=False
        )
        if str(reply.get("success")).lower() == "false":
            raise PnoCommandError(f"setParam {param}={value} -> {reply}")

    #: controller parameter id for master volume (0-100), verified live
    PARAM_MASTER_VOLUME = 47

    async def async_set_volume(self, level: int) -> None:
        """Master volume, 0-100 (param 47).  Verified live."""
        await self.async_set_param(self.PARAM_MASTER_VOLUME, max(0, min(100, int(level))))
