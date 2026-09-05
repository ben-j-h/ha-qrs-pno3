# QRS PNO3 Player Piano — Home Assistant integration

A local-polling custom integration for the **QRS PNOmation³ / PNO3** player-piano
controller. It talks straight to the controller's (undocumented, unauthenticated)
HTTP API on your LAN — no cloud, no QRS account.

> Reverse-engineering notes, endpoint reference and live test results are in
> [`research/`](research/). Start with [`research/README.md`](research/README.md).

## Features

- **`media_player`** entity: play / pause / resume / stop / seek, next / previous,
  volume, mute, repeat, shuffle, turn on/off, **browse & play** the whole library
  (by playlist / artist / album / genre) and `play_media` by musicId or search text.
- **Local library cache** — the ~14 k-song catalog + metadata + playlists are
  mirrored into a small SQLite file so browsing and search are instant and don't
  hammer the slow built-in web app. Kept fresh automatically when the controller
  bumps `libraryVersion` / `tagVersion`.
- **`qrs_pno3.refresh_library`** service (and a button) to force a full cache rebuild.
- Diagnostic **sensors** (faults, warnings, library/tag version, song count,
  download progress), a **rail-power switch**, **clear-faults / panic-stop /
  refresh-cache buttons**, and experimental tempo/transpose **numbers** (disabled
  by default — see caveats).
- Adaptive polling: ~2 s while playing, backing off to ~30 s idle (configurable).

## Requirements

- Home Assistant **2024.12** or newer.
- A PNO3 / PNOmation controller reachable over HTTP on your network
  (tested against web-app version `0.661`).

## Installation

### HACS (custom repository)

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/ben-j-h/ha-qrs-pno3`,
   category **Integration**.
2. Install **QRS PNO3 Player Piano**, restart Home Assistant.
3. **Settings → Devices & Services → Add Integration → QRS PNO3**, enter the
   controller's IP address.

### Manual

Copy `custom_components/qrs_pno3/` into your HA `config/custom_components/`
directory and restart.

## Dashboard

No custom card needed — the entity is a real media player, so the built-in
**Media Control** card handles playback, seek, volume, repeat/shuffle, power and
the media browser (Playlists / Artists / Albums / Genres → songs). It just has no
album art, so the card shows a plain music icon.

Pair it with an entities/tile card for the piano-specific bits:

```yaml
type: vertical-stack
cards:
  - type: media-control
    entity: media_player.pno3_192_168_30_140
  - type: entities
    title: Piano
    entities:
      - switch.pno3_192_168_30_140_solenoid_rail_power
      - sensor.pno3_192_168_30_140_system_faults
      - sensor.pno3_192_168_30_140_system_warnings
      - sensor.pno3_192_168_30_140_library_songs
      - button.pno3_192_168_30_140_clear_faults
      - button.pno3_192_168_30_140_stop_panic
      - button.pno3_192_168_30_140_refresh_library_cache
```

(Enable the `tempo` / `transpose` number entities in the entity settings if you
want them — they're read-only in practice; see the caveats.)

## Options

**Settings → Devices & Services → QRS PNO3 → Configure**

| Option | Default | Notes |
|---|---|---|
| Poll interval while playing | 2 s | position updates |
| Poll interval while idle | 30 s | |
| Full parameter refresh interval | 60 s | pulls master-volume etc. (`all_stream.php?js`, ~290 KB); `0` disables |
| "Turn off" also stops playback | on | |

## Services

| Service | What it does |
|---|---|
| `qrs_pno3.refresh_library` | Full rebuild of the local library cache |
| `qrs_pno3.play_song` | Play by `music_id` **or** free-text `query` |
| `qrs_pno3.send_command` | Advanced: raw pipe-language command (`$\|60000`, `V`, …); checksum added for you |
| `qrs_pno3.set_tempo` / `qrs_pno3.set_transpose` | Experimental parameter writes (see caveats) |
| `qrs_pno3.clear_faults` | `requestType=clrFaults` |

## Known limitations / caveats

These come from live testing — details in
[`research/06-live-test-results.md`](research/06-live-test-results.md):

- **Tempo / transpose writes**: the controller returns `success` but no runtime
  effect was observed. Exposed **read-only** via `media_player` attributes and as
  *disabled-by-default* `number` entities. The reported values still update.
- **Turn off**: `setPower&powerOn=0` is acknowledged but the controller only
  de-energises the solenoid rails on its own idle timer, so the switch/`turn_off`
  may take minutes to reflect. Turning on (and starting playback) is immediate.
- **Next / previous track**: there is no server-side command — the integration
  walks the active playlist (or musicId order) itself. "Previous" restarts the
  current track if you're more than 3 s in.
- No push channel: this is polling. The controller's on-box MQTT broker is not
  exposed to the network.

## Network placement

Nothing this integration does needs internet — it's all LAN. The controller only
needs internet for buying/downloading QRS-catalog music, firmware updates,
streaming "radio", cloud voice assistants and away-from-home app control. It runs
an unauthenticated HTTP API, an old (Dropbear 2017.75) SSH server and an outbound
MQTT bridge to QRS, so an **isolated / no-internet VLAN is recommended** — just
allow your HA host to reach `PNO3:80`, and open egress temporarily when you want
to buy music or update firmware.

You can add your own music locally with no QRS account — accepted types are
`.mid`, `.qrs`, `.mp3`, `.wav`. A plain **Standard MIDI File** is all it takes to
drive the keys (DAW export, MuseScore, a recorded keyboard, SMFs off the net);
`.mp3`/`.wav` play through the speakers only; `.qrs` is QRS's MIDI-plus-expression
format you'll only get from their catalog. Get files onto the piano via USB
import, the on-piano record button, or SFTP into `/media/saved/`. Format details,
limits (this unit drives MIDI notes 25–104, 16 voices) and connectivity notes:
[`research/07-adding-music-and-connectivity.md`](research/07-adding-music-and-connectivity.md).

## Roadmap

Post-`v0.2.x` ideas (test suite, live "keys playing" data + a piano panel card,
cover art, USB-import service, DHCP discovery, …) are in
[`ROADMAP.md`](ROADMAP.md).

## Repo layout

```
custom_components/qrs_pno3/   the integration
research/                     reverse-engineering docs, API reference, samples
```

## Disclaimer

Unofficial. Not affiliated with QRS Music Technologies. The controller API is
undocumented and may change with firmware updates. Playing a song physically
actuates the piano.
