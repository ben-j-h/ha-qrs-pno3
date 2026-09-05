# QRS PNO3 Controller — Reverse-Engineering Notes

Target device: **QRS PNOmation³ (PNO3) controller** driving a baby grand player piano.
Base URL investigated: `http://192.168.0.225`

Date of capture: 2026-09-05. Web app version string: **`v=0.661`** (`WEBAPPV1.00000003`).

---

## TL;DR — what we found

* The controller is an **embedded Linux box** running **lighttpd 1.4.48 + PHP 8.1**. Web root `/usr/www`, app at `/usr/www/qrs`, API at `/usr/www/php`.
* The "app" is a **Sencha Touch 3** single-page app (`/qrs/csrc/all_.js`, `all2_.js`) that is slow purely because it downloads ~2.5 MB of JS + a **1.4 MB tag/metadata blob** + a **~950 KB library index** on every cold load and then re-polls status on a timer. The *backend* itself is fast (server-side timers in responses show 5–100 ms).
* **No authentication anywhere.** Every endpoint is plain HTTP GET/POST on the LAN. Only ports **22 (SSH)** and **80 (HTTP)** are open. The on-box Mosquitto/MQTT broker is **not** exposed to the network (`wsEnabled:false`), so MQTT is not an integration path without SSH tunnelling.
* The library is a **SQLite database** on the controller (PDO/sqlite, schemas `PERSISTENT`, `TEMP`, tables like `MUSIC_LIBRARY`, `TRACK`/playlist tables). It is **not** directly downloadable over HTTP, but its full contents are exposed via JSON endpoints (`music_stream.php`, `tags.php`, `playlist.php`).
* **Playback control is trivial**: single HTTP GETs to `/php/changePlaySettings.php` (XML response) or `/php/changePlaySettingsJSON.php` (JSON response). Play a specific song, stop, pause, power on/off, repeat, shuffle, seek, next/prev.
* **Now-playing state** is available two ways:
  * `GET /php/changePlaySettingsJSON.php?requestType=getStatus` → tiny JSON, includes human‑readable `"Artist - Title (path)"`, `state`, `power`, `faults`.
  * `GET /php/all_stream.php?quick=1&...` → ~2 KB JSON with a full `playbackInformation` object (position ms, duration ms, playlist id/track, music id, tempo, transpose, mutes, faults, download progress, …).

**Conclusion: a Home Assistant integration is very achievable.** See [`05-home-assistant-architecture.md`](05-home-assistant-architecture.md) for the recommended shape (a pure‑Python HA custom integration with a local polling coordinator + a cached SQLite/JSON mirror of the library; **no middleware container required**, though a thin proxy is a reasonable option and is discussed).

---

## Status

The Home Assistant integration is built — see [`../custom_components/qrs_pno3/`](../custom_components/qrs_pno3/)
and the top-level [`../README.md`](../README.md). Write-path commands were verified
against the real piano ([`06-live-test-results.md`](06-live-test-results.md)) and the
parsing / cache logic has an offline check suite at
[`probe/test_units.py`](probe/test_units.py) (33 checks against the captured samples).

## Documents in this folder

| File | Contents |
|------|----------|
| [`01-http-api-reference.md`](01-http-api-reference.md) | Every HTTP endpoint discovered, params, sample responses, error behaviour |
| [`02-playback-state-reference.md`](02-playback-state-reference.md) | `all_stream.php` structure + full `playbackInformation` field dictionary |
| [`03-library-and-metadata.md`](03-library-and-metadata.md) | `music_stream.php`, `tags.php`, `playlist.php`, the file/catalog path scheme, how to join them, incremental-sync (epoch) mechanics, SQLite notes |
| [`04-control-commands.md`](04-control-commands.md) | Transport + settings commands: play/stop/pause/power/repeat/shuffle/seek, volume/tempo/transpose, the `sendCommand` pipe-opcode mini-language |
| [`05-home-assistant-architecture.md`](05-home-assistant-architecture.md) | Architecture options and the recommended design for the custom integration |
| [`06-live-test-results.md`](06-live-test-results.md) | What the write path actually did on the real piano (play/pause/seek/volume/repeat/…), verified quirks |
| [`07-adding-music-and-connectivity.md`](07-adding-music-and-connectivity.md) | How to add your own music locally (USB/SFTP/record), what's DRM-gated, exactly which features need internet, and the recommended VLAN/firewall setup |
| [`settings_dictionary.md`](settings_dictionary.md) | All 1,222 controller parameters (`id → value / range / description`) from `all_stream.php?js` |
| `samples/` | Raw captured JSON/JS responses (used by `probe/test_units.py`) |
| `probe/` | `pno.py` manual CLI + `test_units.py` offline check suite |
| `raw/` | Raw downloaded app bundles (`all_.js`, `all2_.js`, generated PHP-JS) used for the RE — git-ignored (vendor code) |

---

## Device facts captured

| Thing | Value |
|-------|-------|
| HTTP server | `lighttpd/1.4.48`, `X-Powered-By: PHP/8.1.0` |
| Root redirect | `/` → `302` → `/qrs/index.html?v=0.661` |
| Web root / API dir | `/usr/www/` , PHP at `/usr/www/php/` |
| Rootfs | `ubi0:rootfs` 174.8 MB (77% used) — read-mostly embedded FS |
| Media storage | microSD mounted at `/media/microsdp1` (song files live here) |
| Open ports | 22 (SSH), 80 (HTTP). 443/1883/8883/9001/8080 closed |
| Ethernet MAC | `AA:BB:CC:00:00:01` |
| Wi‑Fi MAC | `AA:BB:CC:00:00:02` (client mode, SSID `REDACTED_SSID`, ~-63 dBm) |
| IP (as seen) | `192.168.0.225` (Wi‑Fi client), also has an Ethernet iface |
| Library version | `libraryVersion: 0.438` |
| Tag version | `tagVersion: 0.717` |
| Song count (index) | ~14,336 rows from `music_stream.php?epoch=0` |
| Dealer info baked in | "Example Piano Dealer" / account XX000 (from `all_stream.php`) |
| Frontend | Sencha Touch 3 + Bootstrap + jQuery, ~2.5 MB JS |
| On-box MQTT | Mosquitto present in MIDI routing table but broker **not** on a reachable port |

## Safety note

All reads in this capture were non-destructive. **No playback or settings changes were sent** — triggering `setPlayMode&state=1` will physically make the piano play. Live write-path verification is still pending your go-ahead.
