# Library & Metadata Model

The controller holds the whole music library in an on-box **SQLite** database (PDO `sqlite`, attached schemas `PERSISTENT` / `TEMP`, tables incl. `MUSIC_LIBRARY`, playlist/`TRACK_ID` tables). The DB file is **not** served over HTTP (`/php/db/`, `/db/`, `*.db` all 404). Instead three JSON endpoints expose everything needed:

| Endpoint | Gives you | Size (this unit) |
|---|---|---|
| `music_stream.php?epoch=0&epoch2=0` | musicId ↔ libraryId ↔ file path, with tombstones | ~950 KB, ~14,336 rows |
| `tags.php?epoch=0` | title / artist / genre / album, keyed by catalog + track | ~1.4 MB |
| `playlist.php?function=list` + `…?function=retrieve&id=<n>` | playlists and their track lists | small |

---

## File path / catalog scheme

Song files live on the microSD at:

```
/media/microsdp1/<CATALOG>/<NN>.<ext>
                 ^^^^^^^^^  ^^          CATALOG = 6-digit QRS catalog/album id
                                        NN      = 2-digit track number ("01".."99")
                                        ext     = qrs | mid | mp3
```

Factory demo files: `/usr/factory/noIndexFiles/Sample_*.{qrs,mid,mp3}` (libraryId `5`).

`.qrs` = QRS's MIDI-with-expression piano-roll format. `.mid` = plain MIDI. `.mp3` = audio (played through the controller's line outputs / powered by "MP3" route, not the solenoids).

---

## `music_stream.php` rows

```json
{"d":0,"lid":1,"id":2489,"src":"/media/microsdp1/801341/01.qrs"}
```

| key | meaning |
|---|---|
| `d` | 0 = active, **1 = removed** (keep as tombstone when doing incremental sync; drop from a full rebuild) |
| `lid` | library id. Observed: `0` (12 rows), `1` (14,261 — the real library), `5` (63 — factory samples) |
| `id` | **musicId** — the value you pass to `setPlayMode&songId=` / `playSong(lid,id)` |
| `src` | absolute file path (see scheme above) |

Last array element is the cursor:
```json
{"timeStamp":"'42'","timeStampTemp":"'21'"}
```
→ next call: `music_stream.php?epoch=42&epoch2=21` returns only rows changed since (adds + `d:1` tombstones). `epoch` tracks the committed library, `epoch2` a temp/staging layer.

`music_stream.php` carries **no metadata** (no title/artist). You must join to `tags`.

---

## `tags.php` structure

`tags.php` **requires `epoch`** (bare `?js=true` returns empty — the browser app keeps tags in localStorage and only fetches deltas). Full dump: `tags.php?epoch=0`.

Response body assigns a JS global (strip the `tags=` prefix / trailing `;` to get JSON):

```js
tags = {
  "660010": {
    "alb": "Korean Favorites",
    "2":  { "sng": "Stan",     "art": "Eminem feat. Dido", "gre": "Popular - SyncAlong" },
    "3":  { "sng": "Memories", "art": "Maroon 5",          "gre": "Popular - SyncAlong" },
    "10": { "sng": "All Falls Down", "art": "Alan Walker, Noah Cyrus & Digital Farm Animals feat. Juliander", "gre": "Popular - SyncAlong" }
    // ... key = track number, WITHOUT leading zero
  },
  // ... key = 6-digit catalog id
}
```

* Top-level key = `CATALOG` (matches the folder in `src`).
* `"alb"` = album/collection title for that catalog.
* Numeric keys = track number as a **plain integer string** (`"2"`, not `"02"`).
* `sng` = song title, `art` = artist, `gre` = genre (note the odd key names: sng/art/gre).
* Occasionally `sng` is a number instead of a string (bad data in the source catalog — handle gracefully).

### Join recipe (musicId → display metadata)

```
row  = music_stream[musicId]                       # -> {lid, src}
m    = /media/microsdp1/(\d+)/(\d+)\.\w+/.match(src)
meta = tags[m[1]]?.[String(parseInt(m[2], 10))]    # -> {sng, art, gre}
album = tags[m[1]]?.alb
```

For files that don't match the pattern (factory samples), fall back to the basename.

---

## Playlists

### `playlist.php?function=list`
```json
[
  {"list_id":0,"list":"Classics","IR":0},
  {"list_id":1,"list":"Rock","IR":1},
  {"list":"    Bruno Mars - The Romantic","list_id":null,"itemId":"PL202608",
   "promoId":50,"promoIds":"14369,14370,14371,...","promoInstalled":0,
   "promoPrice":25,"promoStart":"2026-08-01","promoEnd":"2026-09-15"}
]
```
* `list_id` present ⇒ a real, local playlist (`list` = name, `IR` ≈ "is radio"/internal flag).
* `list_id: null` + `promoId` ⇒ a QRS store promo bundle (ignore for control; show in a "store" view if ever wanted).

### `playlist.php?function=retrieve&id=<list_id>`
```json
[{"tid":0,"lid":1,"src":"/media/microsdp1/801237/02.qrs"},
 {"tid":1,"lid":1,"src":"/media/microsdp1/801237/13.qrs"}]
```
`tid` = 0-based position in the playlist. No `id`/musicId here — join `src` back to `music_stream` to get the musicId, then to `tags`.

---

## Incremental sync strategy (for the cached mirror)

1. **Cold build**: `music_stream.php?epoch=0&epoch2=0` + `tags.php?epoch=0` + `playlist.php?function=list` (+ each `retrieve`). Store `epoch`,`epoch2` from the trailer, and `libraryVersion`/`tagVersion` from `all_stream`.
2. **On each poll of `all_stream.php`**: compare `playbackInformation.libraryVersion` / `tagVersion`.
   * `libraryVersion` changed ⇒ `music_stream.php?epoch=<saved>&epoch2=<saved2>` → apply adds, delete `d:1` rows, save new cursor.
   * `tagVersion` changed ⇒ re-fetch `tags.php?epoch=<?>` (tag deltas appear to be keyed similarly; simplest robust approach is a full `tags.php?epoch=0` refetch on version bump — 1.4 MB, infrequent).
3. Playlists have no version field — refetch `list` + changed `retrieve` on a slow timer (e.g. every 30 min) or on demand.

## Suggested cache schema (SQLite in the integration / middleware)

```sql
CREATE TABLE songs (
  music_id     INTEGER PRIMARY KEY,
  library_id   INTEGER,
  src          TEXT,
  catalog      TEXT,        -- parsed from src
  track_no     INTEGER,
  title        TEXT,
  artist       TEXT,
  genre        TEXT,
  album        TEXT,
  removed      INTEGER DEFAULT 0
);
CREATE INDEX ix_songs_artist ON songs(artist);
CREATE INDEX ix_songs_title  ON songs(title);
CREATE INDEX ix_songs_catalog ON songs(catalog);

CREATE TABLE playlists (list_id INTEGER PRIMARY KEY, name TEXT, is_radio INTEGER);
CREATE TABLE playlist_tracks (list_id INTEGER, tid INTEGER, music_id INTEGER,
  PRIMARY KEY (list_id, tid));

CREATE TABLE sync_state (k TEXT PRIMARY KEY, v TEXT);
-- rows: epoch, epoch2, library_version, tag_version, built_at
```

That's ~14k rows — tiny. A full metadata search ("play something by Elton John") becomes a local `SELECT`.
