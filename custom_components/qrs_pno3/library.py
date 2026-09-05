"""Local cached mirror of the PNO3 music library.

The controller keeps ~14k songs in an on-box SQLite DB that is not reachable over
HTTP.  We rebuild an equivalent cache from three JSON feeds
(``music_stream.php`` + ``tags.php`` + ``playlist.php``) and keep it fresh by
watching ``playbackInformation.libraryVersion`` / ``tagVersion``.

All sqlite access runs in the executor - ``sqlite3`` is stdlib, no extra
requirement.
"""

from __future__ import annotations

import logging
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant

from .api import PnoApiClient

_LOGGER = logging.getLogger(__name__)

_SRC_RE = re.compile(r"/([0-9]{3,})/([0-9]+)\.[A-Za-z0-9]+$")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS songs (
    music_id    INTEGER PRIMARY KEY,
    library_id  INTEGER,
    src         TEXT,
    catalog     TEXT,
    track_no    INTEGER,
    title       TEXT,
    artist      TEXT,
    genre       TEXT,
    album       TEXT,
    removed     INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_songs_artist  ON songs(artist);
CREATE INDEX IF NOT EXISTS ix_songs_title   ON songs(title);
CREATE INDEX IF NOT EXISTS ix_songs_genre   ON songs(genre);
CREATE INDEX IF NOT EXISTS ix_songs_album   ON songs(album);
CREATE INDEX IF NOT EXISTS ix_songs_src     ON songs(src);

CREATE TABLE IF NOT EXISTS playlists (
    list_id   INTEGER PRIMARY KEY,
    name      TEXT,
    is_radio  INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS playlist_tracks (
    list_id   INTEGER NOT NULL,
    tid       INTEGER NOT NULL,
    music_id  INTEGER,
    src       TEXT,
    PRIMARY KEY (list_id, tid)
);

CREATE TABLE IF NOT EXISTS sync_state (k TEXT PRIMARY KEY, v TEXT);
"""

_SONG_COLS = "music_id, library_id, src, catalog, track_no, " "title, artist, genre, album, removed"
_INSERT_SONG = f"INSERT OR REPLACE INTO songs ({_SONG_COLS}) VALUES (?,?,?,?,?,?,?,?,?,?)"
_INSERT_PL_TRACK = (
    "INSERT OR REPLACE INTO playlist_tracks (list_id, tid, music_id, src) VALUES (?,?,?,?)"
)


@dataclass(slots=True, frozen=True)
class Track:
    """One playable song from the cache."""

    music_id: int
    library_id: int
    src: str
    title: str
    artist: str
    genre: str
    album: str

    @property
    def display(self) -> str:
        if self.artist and self.title:
            return f"{self.artist} - {self.title}"
        return self.title or self.src.rsplit("/", 1)[-1]


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


class PnoLibrary:
    """Owns the on-disk cache file and all queries against it."""

    def __init__(self, hass: HomeAssistant, api: PnoApiClient, db_path: str) -> None:
        self._hass = hass
        self._api = api
        self._path = db_path

    # -- lifecycle ------------------------------------------------------
    async def async_setup(self) -> None:
        await self._hass.async_add_executor_job(self._setup)

    def _setup(self) -> None:
        Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    # -- build / sync -------------------------------------------------
    async def async_is_populated(self) -> bool:
        return await self._hass.async_add_executor_job(self._is_populated)

    def _is_populated(self) -> bool:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS n FROM songs").fetchone()
        return bool(row and row["n"])

    async def async_rebuild(self) -> dict[str, Any]:
        """Full cold rebuild of the cache.  Backs the ``refresh_library`` service."""
        _LOGGER.info("Rebuilding PNO3 library cache at %s", self._path)
        rows, epoch, epoch2 = await self._api.async_music_stream("0", "0")
        tags = await self._api.async_tags()
        playlists = await self._api.async_playlists()
        pl_tracks: dict[int, list[dict[str, Any]]] = {}
        for pl in playlists:
            lid = pl.get("list_id")
            if isinstance(lid, int):
                pl_tracks[lid] = await self._api.async_playlist_tracks(lid)

        stats = await self._hass.async_add_executor_job(
            self._write_full, rows, tags, playlists, pl_tracks, epoch, epoch2
        )
        _LOGGER.info("PNO3 library cache rebuilt: %s", stats)
        return stats

    def _write_full(
        self,
        rows: list[dict[str, Any]],
        tags: dict[str, Any],
        playlists: list[dict[str, Any]],
        pl_tracks: dict[int, list[dict[str, Any]]],
        epoch: str,
        epoch2: str,
    ) -> dict[str, Any]:
        src_to_id: dict[str, int] = {}
        songs: list[tuple] = []
        for r in rows:
            src = r.get("src", "")
            mid = r.get("id")
            if mid is None:
                continue
            src_to_id[src] = mid
            catalog, track_no = "", None
            m = _SRC_RE.search(src)
            if m:
                catalog, track_no = m.group(1), int(m.group(2))
            meta = tags.get(catalog, {}) if catalog else {}
            album = _clean(meta.get("alb"))
            tmeta = meta.get(str(track_no)) if track_no is not None else None
            tmeta = tmeta if isinstance(tmeta, dict) else {}
            songs.append(
                (
                    int(mid),
                    r.get("lid", 1),
                    src,
                    catalog,
                    track_no,
                    _clean(tmeta.get("sng")),
                    _clean(tmeta.get("art")),
                    _clean(tmeta.get("gre")),
                    album,
                    1 if r.get("d") else 0,
                )
            )

        with self._connect() as conn:
            conn.execute("DELETE FROM songs")
            conn.execute("DELETE FROM playlists")
            conn.execute("DELETE FROM playlist_tracks")
            conn.executemany(_INSERT_SONG, songs)
            for pl in playlists:
                lid = pl.get("list_id")
                if not isinstance(lid, int):
                    continue
                conn.execute(
                    "INSERT OR REPLACE INTO playlists (list_id, name, is_radio) VALUES (?,?,?)",
                    (lid, _clean(pl.get("list")), 1 if pl.get("IR") else 0),
                )
                conn.executemany(
                    _INSERT_PL_TRACK,
                    [
                        (lid, t.get("tid", i), src_to_id.get(t.get("src", "")), t.get("src"))
                        for i, t in enumerate(pl_tracks.get(lid, []))
                    ],
                )
            self._set_state(conn, "epoch", epoch)
            self._set_state(conn, "epoch2", epoch2)

        return {
            "songs": len(songs),
            "playlists": sum(1 for p in playlists if isinstance(p.get("list_id"), int)),
            "epoch": epoch,
        }

    async def async_sync_if_changed(self, library_version: Any, tag_version: Any) -> None:
        """Incremental refresh triggered by a version bump in ``playbackInformation``."""
        state = await self._hass.async_add_executor_job(self._all_state)
        lib_changed = _clean(library_version) not in ("", "0") and _clean(
            library_version
        ) != state.get("library_version")
        tag_changed = _clean(tag_version) not in ("", "0") and _clean(tag_version) != state.get(
            "tag_version"
        )
        if not lib_changed and not tag_changed:
            return

        _LOGGER.info(
            "PNO3 library version change (lib %s->%s, tag %s->%s) - syncing",
            state.get("library_version"),
            _clean(library_version),
            state.get("tag_version"),
            _clean(tag_version),
        )

        if tag_changed or not state.get("epoch"):
            # tag deltas are fiddly; a full rebuild is simplest and infrequent.
            await self.async_rebuild()
        else:
            rows, epoch, epoch2 = await self._api.async_music_stream(
                state.get("epoch", "0"), state.get("epoch2", "0")
            )
            tags = await self._api.async_tags()
            await self._hass.async_add_executor_job(self._apply_delta, rows, tags, epoch, epoch2)

        await self._hass.async_add_executor_job(
            self._set_versions, _clean(library_version), _clean(tag_version)
        )

    def _apply_delta(
        self, rows: list[dict[str, Any]], tags: dict[str, Any], epoch: str, epoch2: str
    ) -> None:
        with self._connect() as conn:
            for r in rows:
                mid = r.get("id")
                if mid is None:
                    continue
                if r.get("d"):
                    conn.execute("UPDATE songs SET removed=1 WHERE music_id=?", (int(mid),))
                    continue
                src = r.get("src", "")
                catalog, track_no = "", None
                m = _SRC_RE.search(src)
                if m:
                    catalog, track_no = m.group(1), int(m.group(2))
                meta = tags.get(catalog, {}) if catalog else {}
                tmeta = meta.get(str(track_no)) if track_no is not None else None
                tmeta = tmeta if isinstance(tmeta, dict) else {}
                conn.execute(
                    _INSERT_SONG,
                    (
                        int(mid),
                        r.get("lid", 1),
                        src,
                        catalog,
                        track_no,
                        _clean(tmeta.get("sng")),
                        _clean(tmeta.get("art")),
                        _clean(tmeta.get("gre")),
                        _clean(meta.get("alb")),
                        0,
                    ),
                )
            self._set_state(conn, "epoch", epoch)
            self._set_state(conn, "epoch2", epoch2)

    # -- sync_state helpers ----------------------------------------
    @staticmethod
    def _set_state(conn: sqlite3.Connection, key: str, value: str) -> None:
        conn.execute(
            "INSERT INTO sync_state (k, v) VALUES (?, ?) "
            "ON CONFLICT(k) DO UPDATE SET v=excluded.v",
            (key, value),
        )

    def _all_state(self) -> dict[str, str]:
        with self._connect() as conn:
            return {row["k"]: row["v"] for row in conn.execute("SELECT k, v FROM sync_state")}

    def _set_versions(self, library_version: str, tag_version: str) -> None:
        with self._connect() as conn:
            if library_version:
                self._set_state(conn, "library_version", library_version)
            if tag_version:
                self._set_state(conn, "tag_version", tag_version)

    # -- queries --------------------------------------------------
    async def async_stats(self) -> dict[str, Any]:
        return await self._hass.async_add_executor_job(self._stats)

    def _stats(self) -> dict[str, Any]:
        with self._connect() as conn:
            songs = conn.execute("SELECT COUNT(*) AS n FROM songs WHERE removed=0").fetchone()["n"]
            artists = conn.execute(
                "SELECT COUNT(DISTINCT artist) AS n FROM songs WHERE removed=0 AND artist<>''"
            ).fetchone()["n"]
            playlists = conn.execute("SELECT COUNT(*) AS n FROM playlists").fetchone()["n"]
            state = {row["k"]: row["v"] for row in conn.execute("SELECT k, v FROM sync_state")}
        return {"songs": songs, "artists": artists, "playlists": playlists, **state}

    async def async_get_track(self, music_id: int) -> Track | None:
        return await self._hass.async_add_executor_job(self._get_track, music_id)

    def _row_to_track(self, row: sqlite3.Row) -> Track:
        return Track(
            music_id=row["music_id"],
            library_id=row["library_id"] if row["library_id"] is not None else 1,
            src=row["src"] or "",
            title=row["title"] or "",
            artist=row["artist"] or "",
            genre=row["genre"] or "",
            album=row["album"] or "",
        )

    def _get_track(self, music_id: int) -> Track | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM songs WHERE music_id=?", (int(music_id),)).fetchone()
        return self._row_to_track(row) if row else None

    async def async_search(self, query: str, limit: int = 50) -> list[Track]:
        return await self._hass.async_add_executor_job(self._search, query, limit)

    def _search(self, query: str, limit: int) -> list[Track]:
        like = f"%{query.strip()}%"
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM songs WHERE removed=0 AND "
                "(title LIKE ? OR artist LIKE ? OR album LIKE ? OR genre LIKE ?) "
                "ORDER BY artist, album, track_no LIMIT ?",
                (like, like, like, like, int(limit)),
            ).fetchall()
        return [self._row_to_track(r) for r in rows]

    async def async_distinct(self, column: str) -> list[str]:
        if column not in ("artist", "album", "genre"):
            raise ValueError(column)
        return await self._hass.async_add_executor_job(self._distinct, column)

    def _distinct(self, column: str) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT DISTINCT {column} AS v FROM songs "
                f"WHERE removed=0 AND {column}<>'' ORDER BY {column} COLLATE NOCASE"
            ).fetchall()
        return [r["v"] for r in rows]

    async def async_by(self, column: str, value: str, limit: int = 500) -> list[Track]:
        if column not in ("artist", "album", "genre"):
            raise ValueError(column)
        return await self._hass.async_add_executor_job(self._by, column, value, limit)

    def _by(self, column: str, value: str, limit: int) -> list[Track]:
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM songs WHERE removed=0 AND {column}=? "
                "ORDER BY album, track_no, title LIMIT ?",
                (value, int(limit)),
            ).fetchall()
        return [self._row_to_track(r) for r in rows]

    async def async_playlists(self) -> list[dict[str, Any]]:
        return await self._hass.async_add_executor_job(self._playlists)

    def _playlists(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM playlists ORDER BY name")]

    async def async_playlist_tracks(self, list_id: int) -> list[Track]:
        return await self._hass.async_add_executor_job(self._playlist_tracks, list_id)

    def _playlist_tracks(self, list_id: int) -> list[Track]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT s.* FROM playlist_tracks pt JOIN songs s ON s.music_id = pt.music_id "
                "WHERE pt.list_id=? ORDER BY pt.tid",
                (int(list_id),),
            ).fetchall()
        return [self._row_to_track(r) for r in rows]

    async def async_next_music_id(
        self, current_music_id: int, *, previous: bool = False
    ) -> int | None:
        """Fallback next/prev: step by musicId order across the whole library."""
        return await self._hass.async_add_executor_job(self._neighbour, current_music_id, previous)

    def _neighbour(self, current: int, previous: bool) -> int | None:
        op, order = ("<", "DESC") if previous else (">", "ASC")
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT music_id FROM songs WHERE removed=0 AND music_id {op} ? "
                f"ORDER BY music_id {order} LIMIT 1",
                (int(current),),
            ).fetchone()
        return row["music_id"] if row else None
