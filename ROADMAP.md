# Roadmap

Ideas for after `v0.2.x`. Nothing here is committed; it's a scratchpad.

## Toward 1.0

- **Real test suite.** Replace `research/probe/test_units.py` with a proper
  `tests/` using `pytest-homeassistant-custom-component` (config-flow tests,
  coordinator with a mocked API, entity state, library sync). Wire it into CI.
- **Decide the fate of tempo / transpose.** `setParam 10000 / 10002` is accepted
  by the controller but has no observed runtime effect. Options: (a) drop the
  `number` entities and keep them as read-only attributes only, (b) keep trying
  to find the real write path — likely `setQuickParam`, or a `sendCommand`
  opcode, or it only takes with a "lock" (`I|1|10001`) set first. Needs more RE
  against the piano while a file is playing.
- **`home-assistant/brands` submission.** Add an icon so the HACS `brands` check
  passes and the `ignore: brands` line can come out of CI.
- **Bake in the min-HA-version claim.** `hacs.json` says `2024.12.0`; only
  `2026.8.1` is actually exercised. Either test against the floor or raise it.

## Features

- **Live "keys playing" data.** `realTime.php` returns `val26`, a 128-element
  boolean vector of which notes are currently sounding (plus `val27` = a
  selected note). Expose it — as a fast-updating attribute or an event — so a
  custom card can draw a live keyboard. Poll it only while `currentPlayerState`
  is playing.
- **Album / cover art.** RE `/php/splash/getImageCover.php` and
  `/php/getImage.php` params and set `media_image_url` so the standard Media
  Control card shows artwork instead of a generic icon.
- **Custom "piano panel" Lovelace card** (optional, only once the above exist):
  transport + tempo/transpose + fault detail + the live keyboard + cover art in
  one card. Not needed for normal use — the built-in Media Control card already
  covers playback.
- **`media_source` integration — probably not.** Registering the library as a
  `media_source` would make piano tracks browsable/playable from *every* player
  (Sonos, cast targets, …), which is usually unwanted — the songs are `.qrs` /
  local paths only the piano can play. The current design deliberately does
  **not** register one: browsing is scoped to the piano's own entity. Only
  revisit this if there's a concrete need, and gate it behind an option.
- **USB import service.** `qrs_pno3.import_usb` wrapping
  `fileUsb.php {record:"copyFromUSB"}` — trigger a copy of a file already on a
  plugged-in USB stick into "My Saved Music". (Can't push bytes over HTTP; no
  upload route on the controller.)
- **Recording control.** Start/stop record, list and (USB-)export recordings
  from `/media/recordings/*.mid`.
- **DHCP discovery.** The controller's hostname is `QRSPNO3` (settings id 44).
  A `dhcp` matcher in `manifest.json` (`hostname: "qrspno3*"`) would let HA
  surface it as a discovered device instead of manual IP entry.
- **Reconfigure flow.** Change the host without remove + re-add.
- **Smarter tag sync.** On a `tagVersion` bump the library currently refetches
  all of `tags.php` (~1.4 MB). Investigate keyed deltas.
- **Playlist playback semantics.** Next/prev currently walks the cached track
  list and issues single-song plays. Evaluate the `P|F|2|<listId>|<idx>` pipe
  form for gapless / shuffle-correct playback of a controller-side playlist.
- **More diagnostics.** Disk-free per mount (from `playbackInformation.drives`),
  MIDI/audio routing, calibration status, Bluetooth pairing requests.

## Nice-to-have

- Handle the driven note range gracefully (this unit: MIDI 25–104, 80 notes,
  16 simultaneous) — surface it, maybe warn on out-of-range `play_media`.
- Options for which optional entities are created.
