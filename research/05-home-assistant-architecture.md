# Home Assistant Integration — Architecture

## What the integration has to do

1. **Poll state** from the controller and expose a `media_player` (+ a few `sensor`/`switch`/`number`/`button` entities).
2. **Send control** (play/stop/pause/seek/power/volume/tempo/repeat/shuffle).
3. **Mirror the library** (~14k songs + metadata + playlists) locally so browsing/searching is instant and doesn't hammer the slow SPA path.
4. Handle the fact that "play" **physically moves the piano** — expose it plainly but don't do surprising things (no auto-play on startup, etc.).

## Key measurements (this unit, on Wi‑Fi)

| Endpoint | Latency | Size | Verdict |
|---|---|---|---|
| `all_stream.php?quick=1&settings=<hi>&…` | **~0.25 s** | ~1.9 KB | ✅ best status poll — rich *and* fastest |
| `changePlaySettingsJSON.php?requestType=getStatus` | ~0.67 s | 0.27 KB | slower (does a DB query); use only as fallback / title source |
| `music_stream.php?epoch=0` | ~1–2 s | ~950 KB | cold sync only |
| `tags.php?epoch=0` | ~1–2 s | ~1.4 MB | cold sync / on `tagVersion` bump |

So: poll `all_stream.php?quick=1` every **2–5 s** while playing, back off to **15–30 s** when idle. Re-sync the library only when `libraryVersion` / `tagVersion` change.

---

## Decision: middleware container or not?

### Recommendation — **native HA custom integration, no container.** 

Everything needed is plain HTTP + JSON that `aiohttp` handles fine, and HA already gives us:
* a `DataUpdateCoordinator` for polling/backoff,
* a config-entry-scoped storage dir for the cached SQLite mirror (`config/.storage/` or the integration's own dir),
* the entity platforms we need.

There is **no protocol translation, no persistent connection, no cross-device fan-out** that would justify a separate service. A container just adds a moving part, its own update lifecycle, and a second network hop.

### When a thin middleware *would* make sense (optional, not required)

* You want the **same cache/API reused by non-HA clients** (a wall tablet dashboard, Node-RED, a Loxone box, scripts).
* You want to **normalise/patch** the controller's quirks (XML→JSON, the `sendCommand` checksum, the tag/`music_stream` join, the DB-query slowness) behind one clean REST/WebSocket API and version it independently of HA releases.
* You want to add **push** (the controller has no webhook/SSE; a small poller could publish MQTT `piano/state` for instant HA updates via MQTT discovery instead of HA polling).

If you go that route: a ~150-line FastAPI (or aiohttp) service in a container that (a) owns the SQLite mirror, (b) exposes `/state`, `/library?q=`, `/playlists`, `/play`, `/stop`, … and optionally (c) publishes `qrs_pno3/state` to your MQTT broker. HA then talks to *that*, or just consumes the MQTT topics. Keep it stateless apart from the cache file.

**Proposed plan: build the native integration first** (it's the smaller surface and directly useful). Factor the controller client + library-sync + metadata-join into a standalone `qrs_pno3` Python package so the exact same code can later be wrapped in a container/MQTT bridge if a second consumer appears.

---

## Native integration shape

```
custom_components/qrs_pno3/
  __init__.py            # setup entry, create coordinator + PnoClient, schedule library sync
  config_flow.py         # host/IP (+ optional name); zeroconf? (device advertises nothing useful — manual IP)
  coordinator.py         # DataUpdateCoordinator: poll all_stream.php?quick=1, adaptive interval
  api.py                 # PnoClient: aiohttp calls, XML+JSON parsing, sendCommand checksum
  library.py             # SQLite mirror: cold build + incremental sync, metadata join, search
  media_player.py        # the main entity
  sensor.py              # faults, warnings, update/download progress, disk free, library/tag version
  switch.py              # rail power, quiet mode, lock tempo, lock transpose
  number.py              # tempo (-100..100), transpose (-24..24), master volume mirror
  button.py              # clear faults, (panic) stop
  media_source.py / browse_media  # browse library by Artist / Album / Genre / Playlist, search
  const.py, manifest.json, strings.json, translations/
```

### `media_player` entity

| Feature | Impl |
|---|---|
| `SUPPORT_PLAY / PAUSE / STOP` | `setPlayMode&state=1/2/0` |
| `SUPPORT_NEXT / PREVIOUS_TRACK` | advance/retreat musicId within `playbackInformation.currentPlaylistId` track list from the mirror; fallback `sendCommand V` |
| `SUPPORT_SEEK` | `sendCommand $|<ms>` |
| `SUPPORT_VOLUME_SET / STEP` | `changeSettingsJSON setParam param=47` (0–100) |
| `SUPPORT_VOLUME_MUTE` | toggle `mute_master` route / stash+restore `param=47` |
| `SUPPORT_REPEAT_SET` | `setRepeat val=0/1/2` |
| `SUPPORT_SHUFFLE_SET` | `setShuffle val=0/1` |
| `SUPPORT_TURN_ON / OFF` | `setPower powerOn=1/0` |
| `SUPPORT_PLAY_MEDIA` | `media_content_id` = `song:<musicId>` or `playlist:<listId>` → play form; also accept an artist/title search string |
| `SUPPORT_BROWSE_MEDIA` | tree from the SQLite mirror: Playlists / Artists / Albums / Genres / All songs |
| state | `currentPlayerState` (+ `currentPowerOn`) → `playing`/`paused`/`idle`/`off` |
| `media_position`/`media_duration` | `currentTrackProgrssMs`/`currentTrackDurationMs` ÷ 1000; set `media_position_updated_at` each poll |
| `media_title`/`media_artist`/`media_album_name`/`media_playlist` | metadata join on `filePath`; fallback parse `getStatus.song` |
| extra_state_attributes | `music_id`, `library_id`, `catalog`, `genre`, `tempo`, `transpose`, `system_faults`, `system_warnings` |

### Coordinator polling

* Primary: `GET all_stream.php?quick=1&settings=<last>&state=<last>&fullCount=<last>&demoCount=<last>&tempCount=<last>&date=<ms>`.
* Parse the `id:-1` element; keep `system_state` / `system_settings` for the next request; apply `{id,val}` deltas to a settings cache (so `param 47` master volume, `10000` tempo, `10002` transpose stay fresh without extra calls).
* Adaptive interval: 2 s if `currentPlayerState==1`, else 5 s if power on / recent activity, else 20–30 s.
* On `libraryVersion` / `tagVersion` change → fire a background library re-sync task (not on the poll thread).
* Be resilient: the box drops Wi‑Fi packets (~8% RX drop observed) — treat timeouts as "unknown, retry", don't thrash entities to `unavailable` on a single miss.

### Library sync (`library.py`)

* Cold: `music_stream.php?epoch=0&epoch2=0` → rows; `tags.php?epoch=0` → metadata; `playlist.php?function=list` + `retrieve` per list. Build the SQLite file described in [`03-library-and-metadata.md`](03-library-and-metadata.md). Store `epoch`,`epoch2`,`library_version`,`tag_version`.
* Incremental: on version bump, `music_stream.php?epoch=<saved>&epoch2=<saved2>` (apply adds, honour `d:1` deletes); refetch `tags.php?epoch=0` on `tagVersion` bump (simple + rare).
* Expose `search(query)`, `by_artist()`, `by_album()`, `by_genre()`, `playlist_tracks(list_id)` for browse/play_media.

### Config flow

* Just **host/IP** + optional friendly name. The device advertises no useful mDNS/SSDP, so manual entry (with a connectivity check hitting `all_stream.php?quick=1`).
* Options: poll intervals, whether `turn_off` also stops playback, enable/disable the calibration-adjacent `number` entities.

---

## Open items to confirm live (needs your OK — these move the piano)

1. `setPlayMode&state=2` really = **pause** (resume keeps position) vs. just stop. (`swapPlay()` in the app implies pause.)
2. Exact **`sendCommand` checksum** convention (sum of ASCII of non-`|` chars) — verify with a seek.
3. `playSource=F` + `libraryId`/`songId` restart semantics; what `restart=0` does (resume?).
4. Whether `setPower powerOn=0` while playing stops gracefully.
5. `repeat`/`shuffle` — do they persist across songs and survive a new `play_media`?
6. Volume: does `param=47` take effect immediately mid-song; does the value round-trip in `all_stream` deltas.
7. Playlist playback: is the plain "iterate musicIds" approach enough, or do we need the `P|F|2|<id>|<idx>` pipe form for gapless/shuffle-correct behaviour.

Once you're ready I can drive these one at a time against the real piano and lock the doc down, then scaffold the integration.
