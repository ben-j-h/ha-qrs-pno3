# Adding music & internet dependency

Findings from the app bundles + live probes. Short version:

* **Your own MIDI/MP3/WAV/QRS files → yes, locally, no QRS account.** Via USB import, on-piano recording, or SFTP into `/media/saved/`.
* **The QRS commercial catalog → only through QRS** (store purchase → DRM key sync → rsync download).
* **Nothing you need day-to-day needs internet.** Local playback + the HA integration are 100% LAN. Internet is only for buying music, updates, streaming radio, cloud voice, and away-from-home app control. **Put it on a no-internet VLAN.**

---

## The on-box "libraries" (relation types)

The app groups content into `rel` types, derived from the file path:

| `rel` | Name in UI | Path prefix | DRM | How it gets there |
|------:|------------|-------------|-----|-------------------|
| 0 | Media Library | `/media/microsdp1/<catalog>/` | **yes** | QRS servers (rsync/FTP) |
| 2 | Unlocked Music | same, gated by unlock code | **yes** (key stored locally) | QRS store purchase + `file_syncer.php?function=syncServerDrm` |
| 1 | **My Saved Music** | `/media/saved/<genre>/<album>/` | **no** | USB import / SFTP |
| 3 | Recordings / Test | `/media/recordings/YYYY_MM_DD_*.mid`, `/media/testfiles/` | no | on-piano record button; factory |

Accepted file types for saved music: **`.mp3`, `.wav`, `.mid`, `.qrs`** (`qrs.musicTypes`).

For **saved** music the metadata (album/genre/artist/track) is parsed from the
**path and filename** (`saved/<Genre>/<Album>/<NNN Title>.mid`, or `... <Artist> - <Title>.mid`)
- there is no tag-DB entry to create. The controller re-scans and indexes these
folders (`playbackInformation.index` = "indexing running"); new files then show up
in `music_stream.php` like any other song.

## Ways to add your own music

### 1. USB import (supported, no account)
Put files on a USB stick → plug into the PNO3 → in the web UI pick a file → **"Copy To My Saved Music"**. Under the hood:
```
POST /php/fileUsb.php   {"record":"copyFromUSB", "file":"<usb path>"}   (or "_all_")
```
→ copies into `/media/saved/`, then re-index. `copyToUSB` / `_all_recordings_` exports the other way. (`fileUsb.php` has crude input validation - a bad body returns *"What do you think you are doing?"* - but no real auth.)

### 2. Record on the piano
The record button captures a live performance to `/media/recordings/*.mid`, auto-indexed, exportable to USB.

### 3. SFTP (port 22 is open)
SSH server is **Dropbear 2017.75**. If you have/guess the root credentials you can `scp`/`sftp` files straight into `/media/saved/<Genre>/<Album>/` and let the indexer pick them up. (Old Dropbear = yet another reason to keep it off the internet.)

### 4. From Home Assistant
The integration can *trigger* a USB copy (`fileUsb.php copyFromUSB`) but **cannot upload a file over HTTP** - there is no multipart upload route in the controller. A `qrs_pno3.import_usb` service is a possible future addition; pushing arbitrary bytes is not.

### What you can't get locally
New **QRS-catalog** titles. That content is licensed + DRM-gated and only QRS's
store + rsync delivers it. (A `.qrs` file from elsewhere dropped in `/media/saved/`
will *play* - it's just MIDI-with-expression - you just won't get QRS's catalog
that way.)

---

## Internet dependency

### Needs internet (all optional / occasional)
| Feature | Endpoint(s) |
|---|---|
| Buy + download QRS catalog music | rsync/FTP to QRS (`Use Rsync`, `rsyncCurrentMedia`, `ftpLog.php`) |
| Sync DRM unlock keys after a purchase | `file_syncer.php?function=syncServerDrm` ("Sync Keys From Server" - button hidden when offline) |
| Create / manage QRS account | `webSave2.php` (first/last/user/pass/email/…) |
| Firmware / library / tag updates | `bootApply.php`, `checkUpdateTable`, smart-board reprogram |
| QRS "radio" streaming | `fileio/radioSwitch.php`, stream sources |
| Away-from-home control via the QRS mobile app | QRS cloud + the on-box **Mosquitto** bridge ("Mosquitto Server Out") |
| Alexa / Google Assistant voice | `aws/checkKey.php`, `aws/checkGKey.php`, `listenerAlexa` |
| Remote dealer support | `remoteSsh` tunnel |
| "You can buy this" hints, online status | `pno3Online.php` (qrsmusic.com), `qrs.na` list, `isOnline.php`, splash images |

### Does NOT need internet
* Playing anything already on the box (catalog, unlocked, saved, recordings)
* The local web UI
* Local-network control from the QRS app or **this HA integration** - all LAN
* DRM'd content keeps playing: unlock keys are downloaded once and stored locally, and the app degrades gracefully offline. (Player pianos are built for spotty wifi. Not 100%-provable there's no periodic re-check - worth blocking egress for a week and trying a locked track.)

### Clock
No NTP logic in the app - time comes from `setClock.php` (the browser pushes its
clock) or OS-level NTP. On a no-internet VLAN with no local NTP the RTC will
drift; only matters for scheduled playback or recording timestamps. Give the VLAN
a local NTP server, allow outbound udp/123, or just open the web UI now and then.

---

## Recommended network placement

**No-internet device VLAN.** Reasons: undocumented embedded Linux, PHP 8.1 with
`display_errors` on, **zero auth on the entire HTTP API**, Dropbear 2017.75 SSH
exposed, and an always-on outbound MQTT bridge to QRS cloud. Nothing you need
daily is lost.

Firewall rules:
| Direction | Rule | Why |
|---|---|---|
| HA host → `PNO3:80/tcp` | allow | integration polling + control across VLANs |
| admin host → `PNO3:22/tcp` | allow (optional) | SFTP music drops |
| `PNO3 → <local NTP>:123/udp` | allow (optional) | keep the clock honest |
| `PNO3 → any` | **deny** (default) | everything else |

When you want to buy/download music or update firmware: temporarily lift egress
(or park it on a trusted VLAN for an hour), do the purchase + `syncServerDrm` +
rsync, then move it back - it plays that content offline afterward.

In HA the `Internet` / `internetAccess` attributes will read `false` on the
isolated VLAN. That's expected and harmless.
