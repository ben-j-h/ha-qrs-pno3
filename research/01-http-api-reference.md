# PNO3 HTTP API Reference

All endpoints are under `http://<controller>/php/…` unless noted. No auth. Mostly `GET` with query-string params. Responses are XML, JSON, or (a few) HTML fragments meant to be `eval`'d / injected by the Sencha app.

PHP `display_errors` is **on**, so malformed requests leak `Warning:`/`Fatal error:` lines with source file paths and line numbers (useful for RE, noisy for parsing — send the right params).

Legend: ✅ verified live · 🔶 seen in app code, not yet hit live · ⚠️ physically actuates the piano

---

## 1. Bootstrap / app assets (for reference only)

| Path | Notes |
|------|-------|
| `GET /` | 302 → `/qrs/index.html?v=0.661` |
| `GET /qrs/index.html?v=0.661` | SPA shell |
| `GET /qrs/csrc/all_.js` `all2_.js` | compiled Sencha app (~790 KB + ~435 KB) — the RE source |
| `GET /qrs/csrc/languages_.js` | picks `../languages/<lng>_.js` |
| `GET /php/splash/getSplash.php` | preloads splash images, sets `splashScreen` flag |
| `GET /php/tags.php?js=true` | metadata blob (see below) |
| `GET /php/all_stream.php?js` | **defines `qrs.vals`** = full settings dictionary array (see `settings_dictionary.md`) + trailing bootstrap JS |

---

## 2. Status / read endpoints

### 2.1 `GET /php/changePlaySettingsJSON.php?requestType=getStatus` ✅  ← best "now playing"
Tiny JSON. Example captured:
```json
{
  "success": false, "message": "Failed to Update!",   // 'success/message' noise – ignore
  "requestType": "getStatus",
  "textColor": "black", "backColor": "green",
  "status": "Okay",
  "playTime": "0:00",
  "song": "Barnabas Fekete - 1900 Love Song (/media/microsdp1/801341/01.qrs)",
  "state": 0,          // 0 = stopped, 1 = playing, 2 = paused
  "power": 0,          // 0/1 solenoid rail power
  "faults": 0,
  "warnings": 0
}
```
The XML sibling `GET /php/changePlaySettings.php?requestType=getStatus` returns:
```xml
<response><success>true</success><textColor>black</textColor><backColor>green</backColor>
<status>Okay</status><elapsed>0:00</elapsed></response>
```
(may be followed by a non-fatal PDO error about `PERSISTENT.MUSIC_LIBRARY` when nothing is loaded — the useful fields come first).

### 2.2 `GET /php/all_stream.php` ✅  ← full machine state
Primary status feed. Query params (all optional; pass `-1` or `0` to "get everything"):

| param | meaning |
|-------|---------|
| `quick` | `1` = state-only lightweight poll, `0` = include settings deltas |
| `settings` | last settings epoch you've seen (`system_settings`) — server returns only newer |
| `state` | last state epoch (`system_state`) |
| `fullCount`, `demoCount`, `tempCount` | other incremental counters |
| `date` | cache-buster |

Response is a JSON **array**. Leading elements are settings deltas `{"id":<paramId>,"val":<n>}` (ids map to `settings_dictionary.md`). The final element `{"id":-1, …}` carries the real payload:
```jsonc
{
  "id": -1,
  "system_state": "'100'",       // bump these back as ?state= / ?settings=
  "system_settings": "'2'",
  "playbackInformation": { … see 02-playback-state-reference.md … },
  "timers": { "getParams": {"time":0.089}, … }   // server-side timing, handy for perf
}
```
When called with a **high** `settings`/`fullCount` (already-current), the response is ~1.9 KB: a handful of always-present settings ids (`56, 446, 10000-10003, 10006, 10007`) + the `playbackInformation` object. This is the efficient poll shape for HA.

The **full** (`?quick=0&settings=0&state=0&fullCount=0`) response is ~183 KB and additionally contains: `currentAudioRoute[]`, full **MIDI routing table** (`SOURCE`/`SINK`/`CHANNEL`/`ROUTE_DELAY`, includes "Mosquitto In/Out", "Piano", "Software Synthesizer", "5-Pin MIDI Out", "USB Device 1/2 Out", "Bluetooth Midi Out"), `fileTranslationCurve[]`, `dealerInformation[]`, `cloudInformation`, `networkConnection` (MAC/IP/gw/DNS/`wapPresent`), `userInformation`.

### 2.3 `GET /php/realTime.php` ✅  ← lightweight diagnostic poll (~1.2 KB, ~500 ms budget in app)
JSON `{"val0":…,"val43":…}`. Used by the app only inside the key-calibration screens. Partially decoded:

| key | observed | likely meaning |
|-----|----------|----------------|
| `val0`–`val2` | bool | status flags (power / activity / fault-ish) |
| `val3` | `[bool,bool,bool]` | 3-lamp / 3-rail state |
| `val5` | `3` | possibly current playlist type |
| `val7` | `19` | possibly current playlist track id (matches `currentPlaylistTrackId`) |
| `val15`,`val16` | floats `0.25`,`0.15` | timing/percent |
| `val24` | `21` | min PNOScan note (matches setting id 1) |
| `val26` | **128-element bool array** | **live per-note key on/off vector** (great for a "keys playing" visual) |
| `val27` | `255` | currently-selected note in key-adjust UI (`255`/`>=128` = none) |
| `val42`,`val43` | `0` | key-adjust cursor / pedal |

Treat `realTime.php` as *diagnostics*; `all_stream.php` is authoritative for playback.

### 2.4 `GET /php/sbInfo.php` ✅  — smart driver board
```json
{"status":"success","smart_board_program_info":[{"DESCRIPTION":"Smart Driver Board Setting is Set to None","BOARD_ID":"","LAST_STATUS":""}],"smart_board_program_infoCount":0}
```

### 2.5 `GET /php/online/testOnline.php` ✅  — connectivity diagnostics
Full JSON of interface state, SSID, signal, packet-drop counters, gateway/DNS, "Device is Online", etc.

### 2.6 `GET /php/isOnline.php` ✅ — returns empty body (200). `GET /php/logger.php?method=…` client log sink (returns `0`).

### 2.7 `GET /php/drmList.php` ✅ — returns an **HTML fragment** (Ext markup) listing unlock/feature codes and music IDs in a DRM list. Not needed for basic control.

---

## 3. Library / metadata endpoints

### 3.1 `GET /php/music_stream.php?epoch=<t>&epoch2=<t>` ✅  ← the library index
`epoch=0&epoch2=0` returns **everything**. JSON array of:
```json
{"d":0,"lid":1,"id":2489,"src":"/media/microsdp1/801341/01.qrs"}
```
* `d` – 0 = present, 1 = removed/tombstone
* `lid` – library id (`0`,`1` main, `5` = factory `/usr/factory/noIndexFiles/*` samples)
* `id` – **musicId** (use with `playSong`/`setPlayMode&songId=`)
* `src` – file path on the controller

Final array element is the epoch cursor: `{"timeStamp":"'42'","timeStampTemp":"'21'"}` → feed back as `epoch=42&epoch2=21` for deltas only. (~14,336 song rows in this unit; ~950 KB.)

### 3.2 `GET /php/tags.php?epoch=0` ✅  ← titles / artists / genres  (also `?js=true&epoch=0`)
> **Needs an `epoch` param or it returns an empty body.** `?js=true` alone (as index.html calls it) returns empty because the client caches tags in localStorage and only pulls deltas; pass `epoch=0` for a full dump.

Assigns a JS global:
```js
tags = {
  "660010": {                       // 6-digit catalog / album folder number
    "alb": "Korean Favorites",
    "2":  {"sng":"Stan","art":"Eminem feat. Dido","gre":"Popular - SyncAlong"},
    "3":  {"sng":"Memories","art":"Maroon 5","gre":"Popular - SyncAlong"},
    …                               // key = track number (no leading zero)
  },
  …
}
```
Join with `music_stream`: parse `src` `/media/microsdp1/<CATALOG>/<NN>.qrs` → `tags[CATALOG][String(parseInt(NN))]`. (~1.4 MB full dump.)

### 3.3 `GET /php/playlist.php?function=list` ✅
```json
[{"list_id":0,"list":"Classics","IR":0},
 {"list_id":1,"list":"Rock","IR":1},
 {"list":"    Bruno Mars - The Romantic","list_id":null,"itemId":"PL202608","promoId":50,
  "promoIds":"14369,14370,…","promoPrice":25,"promoStart":"2026-08-01","promoEnd":"2026-09-15"}, …]
```
Rows with `list_id` = real local playlists; rows with `list_id:null` + `promoId` = store promos.

### 3.4 `GET /php/playlist.php?function=retrieve&id=<list_id>` ✅
```json
[{"tid":0,"lid":1,"src":"/media/microsdp1/801237/02.qrs"},
 {"tid":1,"lid":1,"src":"/media/microsdp1/801237/13.qrs"}, …]
```
`tid` = track index within the playlist, `src` = file path (join to `music_stream` on `src` to get the `id`, then to `tags` for metadata).

> Calling `playlist.php` with **no** `function` triggers `Undefined array key "function"/"id"` warnings and a `PDOException … near "="` — harmless, just pass the params. Confirms a **SQLite** backend (`PDO->query('SELECT TRACK_ID …')`).

### 3.5 🔶 Other library writers seen in app code (not exercised)
`playlist.php` also supports create/add/delete/reorder (`function=` variants), `delete.php` (remove downloaded music), `fileUsb.php` (USB import/export), `drmList.php` / `orderDrmCheck.php` (unlocks), `pnoCloudSave.php` / `pnoCloudSendFile.php` (QRS cloud sync). Out of scope for a controller; document later if needed.

---

## 4. Control endpoints (write) — see `04-control-commands.md` for the full command set

| Endpoint | Response | Use |
|----------|----------|-----|
| `GET /php/changePlaySettings.php?…` | XML `<response><success/>…` | transport: play/stop/pause/power/repeat/shuffle/seek/next/prev, `sendCommand` |
| `GET /php/changePlaySettingsJSON.php?…` | JSON | same, JSON response (nicer for middleware) |
| `GET /php/changeSettings.php?requestType=setParam&param=<id>&val=<v>` | XML | controller params (calibration, routes, …) |
| `GET /php/changeSettingsJSON.php?requestType=setParam|setQuickParam&param=<id>&val=<v>` | JSON | **volume (id 47), tempo (10000), transpose (10002), EQ (48/49/50)** |
| `GET /php/changeModulation.php?id=<n>[&value=<v>]` | JSON | per-channel modulation/volume mix; GET without `value` reads |
| `POST /php/changeSettingsJSON.php` (jsonData) | JSON | bulk `record:"deleteCache"` etc. |
| `GET /php/setClock.php` 🔶 | — | set RTC |
| `GET /php/netApply.php` / `bootApply.php` 🔶 | — | apply network / boot settings (**reboots/reconfigures — avoid**) |
| `GET /php/wifi/ssidList.php` 🔶 | — | scan Wi‑Fi |
| `GET /php/fileio/radioSwitch.php` 🔶 | — | QRS "radio" station switch |

### `requestType` values seen for `changePlaySettings*.php`
`setPlayMode`, `setPower`, `setRepeat`, `setShuffle`, `setSeek`(via `sendCommand $|`), `sendCommand`, `clrFaults`, `getStatus`.

### `requestType` values seen for `changeSettings*.php`
`setParam`, `setQuickParam`, `setNote`, `setPedal`, `setRange`, `setCurve`, `setDacCurves`, `setVoice`, `setPower`, `setSynth`, `setExtend`, `setExtendMinMid`, `setGlobal`, `setGlobalMinMid`, `setRoutesTable`, `setAudioRouterAll`, `setAllNoteParam`, `getParam`, `getStatus`, `clrFaults`, `killAll`.

---

## 5. Error/'404' behaviour

* Unknown path → lighttpd XHTML `404 - Not Found` page (`Content-Length: 345`).
* `changeSettings.php` with no `requestType` → `<response><success>false</success><message>Invalid request type given!</message></response>` preceded by ~30 `Warning:` lines.
* Endpoints that hit an unattached SQLite schema when idle emit `PDOException: … no such table: PERSISTENT.MUSIC_LIBRARY` — cosmetic when the front matter already returned.
