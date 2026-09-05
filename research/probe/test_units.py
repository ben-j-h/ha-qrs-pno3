#!/usr/bin/env python3
"""Offline unit checks for the integration's pure logic.

Stubs `homeassistant.*` just enough to import `api` and `library`, then runs the
JSON parsing / checksum / SQLite-cache logic against the real captured samples in
research/samples/.  Not a pytest suite - just `python3 test_units.py`.
"""

from __future__ import annotations

import asyncio
import pathlib
import sys
import types

ROOT = pathlib.Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "research" / "samples"
CC = ROOT / "custom_components"

# --- stub homeassistant.core -------------------------------------------------
ha = types.ModuleType("homeassistant")
ha_core = types.ModuleType("homeassistant.core")


class HomeAssistant:  # minimal
    async def async_add_executor_job(self, func, *args):
        return func(*args)


ha_core.HomeAssistant = HomeAssistant
ha.__path__ = []  # mark as package
ha.core = ha_core
sys.modules["homeassistant"] = ha
sys.modules["homeassistant.core"] = ha_core

# Fake, empty `qrs_pno3` package so importing submodules does NOT run the real
# __init__.py (which pulls in the rest of Home Assistant).
pkg = types.ModuleType("qrs_pno3")
pkg.__path__ = [str(CC / "qrs_pno3")]
sys.modules["qrs_pno3"] = pkg

from qrs_pno3.api import PnoApiClient, pno_checksum  # noqa: E402
from qrs_pno3.library import _SRC_RE, PnoLibrary  # noqa: E402

PASS = 0
FAIL = 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok   {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name} {extra}")


# --- checksum --------------------------------------------------------------
print("checksum")
check("seek $|60000 -> 282|$|60000", pno_checksum("$|60000") == "282|$|60000")
check("V -> 86|V", pno_checksum("V") == "86|V")
check(
    "lock tempo I|1|10001 -> 364|I|1|10001",
    pno_checksum("I|1|10001") == "364|I|1|10001",
    pno_checksum("I|1|10001"),
)
check(
    "multi S__P|F|1|0|3 keeps __",
    pno_checksum("S__P|F|1|0|3").count("__") == 1
    and pno_checksum("S__P|F|1|0|3").startswith("83|S__"),
    pno_checksum("S__P|F|1|0|3"),
)

# --- src regex ----------------------------------------------------------
print("src parsing")
m = _SRC_RE.search("/media/microsdp1/801341/01.qrs")
check("catalog/track from qrs path", bool(m) and m.group(1) == "801341" and m.group(2) == "01")
check("factory path yields no match", _SRC_RE.search("/usr/factory/noIndexFiles/Sample_QRS.qrs") is None)


# --- fake aiohttp session serving the sample files ----------------------
class FakeResp:
    def __init__(self, text):
        self._t = text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    def raise_for_status(self):
        pass

    async def text(self):
        return self._t


class FakeSession:
    def __init__(self, routes):
        self.routes = routes
        self.seen = []

    def get(self, url, timeout=None):
        s = str(url)
        self.seen.append(s)
        for frag, path in self.routes.items():
            if frag in s:
                return FakeResp(pathlib.Path(path).read_text(encoding="utf-8", errors="replace"))
        raise AssertionError(f"unrouted URL {s}")


async def main() -> None:
    routes = {
        "all_stream.php?quick=1": SAMPLES / "all_stream_quick.json",
        "all_stream.php?quick=0": SAMPLES / "all_stream_full.json",
        "all_stream.php?js": SAMPLES / "settings_dictionary.js",
        "music_stream.php": SAMPLES / "music_stream_epoch0.json",
        "tags.php": SAMPLES / "tags_epoch0.js",
        "playlist.php?function=list": SAMPLES / "playlist_list.json",
        "playlist.php?function=retrieve": SAMPLES / "playlist_retrieve_id1.json",
    }
    session = FakeSession(routes)
    api = PnoApiClient("192.0.2.1", session)

    print("api.async_quick_state")
    pb, deltas, ss, sset = await api.async_quick_state()
    check("playback has currentMusicId 2489", pb.get("currentMusicId") == 2489)
    check("player state present", "currentPlayerState" in pb)
    check("deltas parsed (id 10000 tempo)", 10000 in deltas, deltas)
    check("system_state stripped of quotes", "'" not in ss and ss != "", repr(ss))

    print("api.async_network_info")
    net = await api.async_network_info()
    check("network info has a mac", bool(net.get("mac")), net)
    check("mac looks like a mac", len(str(net.get("mac", "")).split(":")) == 6, net.get("mac"))

    print("api.async_all_params")
    params = await api.async_all_params()
    check("param 47 master volume present", 47 in params, list(params)[:5])
    check("param 47 value is 50", params.get(47) == 50, params.get(47))
    check("~1200 params", len(params) > 1000, len(params))

    print("api.async_music_stream")
    rows, e1, e2 = await api.async_music_stream("0", "0")
    check("music rows > 14000", len(rows) > 14000, len(rows))
    check("row has id+src+lid", all(k in rows[0] for k in ("id", "src", "lid")))
    check("epoch cursor extracted", e1 == "42" and e2 == "21", (e1, e2))

    print("api.async_tags")
    tags = await api.async_tags()
    check("tag catalog 801341 present", "801341" in tags)
    check(
        "801341 track 1 title",
        tags.get("801341", {}).get("1", {}).get("sng") == "1900 Love Song",
        tags.get("801341", {}).get("1"),
    )

    print("api.async_playlists / tracks")
    pls = await api.async_playlists()
    check("playlist list parsed, has Rock", any(p.get("list") == "Rock" for p in pls))
    pltr = await api.async_playlist_tracks(1)
    check("playlist 1 tracks have src", pltr and "src" in pltr[0])

    # --- library cache end to end ------------------------------------
    print("PnoLibrary rebuild + query (real sample data)")
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        lib = PnoLibrary(HomeAssistant(), api, str(pathlib.Path(td) / "cache.db"))
        await lib.async_setup()
        stats = await lib.async_rebuild()
        check("rebuild wrote > 14000 songs", stats["songs"] > 14000, stats)

        t = await lib.async_get_track(2489)
        check("get_track 2489 -> Barnabas Fekete", t is not None and t.artist == "Barnabas Fekete", t)
        check("get_track 2489 title", t and t.title == "1900 Love Song", t and t.title)
        check("track.display formats", t and t.display == "Barnabas Fekete - 1900 Love Song")

        hits = await lib.async_search("1900 Love Song")
        check("search finds it", any(h.music_id == 2489 for h in hits), len(hits))

        artists = await lib.async_distinct("artist")
        check("distinct artists non-empty + sorted", len(artists) > 100 and artists == sorted(artists, key=str.lower))

        by = await lib.async_by("artist", "Barnabas Fekete")
        check("by artist returns multiple", len(by) >= 5, len(by))

        nxt = await lib.async_next_music_id(2489)
        check("next music id > 2489", nxt is not None and nxt > 2489, nxt)
        prv = await lib.async_next_music_id(2489, previous=True)
        check("prev music id < 2489", prv is not None and prv < 2489, prv)

        st = await lib.async_stats()
        check("stats has songs+artists+playlists", {"songs", "artists", "playlists"} <= set(st), st)

        # incremental: same versions -> no-op; new version -> rebuild path
        await lib.async_sync_if_changed("0.438", "0.717")
        st2 = await lib.async_stats()
        check("sync no-op keeps songs", st2["songs"] == st["songs"])

    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)


asyncio.run(main())
