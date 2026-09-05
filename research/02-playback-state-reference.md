# Playback / System State Reference (`all_stream.php`)

`GET /php/all_stream.php` returns a JSON **array**. The element with `"id": -1` is the state payload:

```jsonc
{
  "id": -1,
  "system_state":    "'100'",   // opaque epoch — echo back as ?state=
  "system_settings": "'2'",     // opaque epoch — echo back as ?settings=
  "playbackInformation": { ... },
  "timers": { "<phase>": {"time": <seconds>}, ... }   // server self-timing
}
```
Elements *before* `id:-1` are settings deltas: `{"id": <paramId>, "val": <number>}` where `paramId` indexes [`settings_dictionary.md`](settings_dictionary.md). Always-present ones in a "quick" poll: `56` (= web version, 0.661), `446`, `10000` tempo, `10001` tempoPersist, `10002` transpose, `10003` transposePersist, `10006`, `10007`.

---

## `playbackInformation` — field dictionary

Values below are from a live capture with the piano **idle** (nothing playing, rail power off). Types inferred from Sencha app usage.

### Transport / now-playing (the important bits for HA)

| Field | Type | Meaning / notes |
|-------|------|-----------------|
| `currentPlayerState` | int | **0 = stopped, 1 = playing, 2 = paused.** (`swapPlay()` toggles 1↔2; `setPlayState(0)` = stop.) |
| `currentStatus` | int | secondary status/mode code (0 when idle) |
| `currentPowerOn` | bool | solenoid rail power energised |
| `currentTrackProgrssMs` | int | playback position, ms (note the misspelling "Progrss"). `<0` = loading/seeking sentinel |
| `currentTrackDurationMs` | int | track length, ms |
| `filePath` | string | path of the loaded/last track, e.g. `/media/microsdp1/801341/01.qrs` → join to `tags` for title/artist |
| `currentMusicId` | int | musicId of loaded track (matches `id` in `music_stream.php`) |
| `currentLibraryId` | int | library id (matches `lid`) |
| `currentPlaylistType` | int | 1 = radio/stream, 2 = user playlist, 3 = "all songs"/browse (observed 3 idle) |
| `currentPlaylistId` | int | active playlist `list_id` |
| `currentPlaylistTrackId` | int | index within the active playlist (observed 19) |
| `playListName` | string | e.g. `"Rock"` |
| `repeat` | int | 0 = off, 1 = repeat-one, 2 = repeat-all |
| `shuffle` | int | 0 / 1 |
| `radioMode` | int | 0 / 1 (QRS "radio" streaming active) |
| `tempo` | int | current tempo offset, **percent** (−100…+100; app converts to BPM via `calculateBMS`). Setting id `10000` |
| `transpose` | int | current transpose, **semitones** (−24…+24). Setting id `10002` |
| `tempoPersist` / `transposePersist` | int | "locked" tempo/transpose applied to all files. Setting ids `10001` / `10003` |
| `recordingInProgress` | bool | a record session is active |
| `lastPlayed` / `lastDropped` | int | last note played / dropped counters (perf) |

### Faults / health

| Field | Type | Meaning |
|-------|------|---------|
| `systemFaults` | int | fault bitmask/count (0 = ok). Clear with `requestType=clrFaults` |
| `systemWarnings` | int | warning count |
| `calibrationStatus` | int | 0 = ok |
| `lastUpdateStatus` | int | last firmware/library update result code |
| `lastFtpStatus` | int | last FTP/sync result |
| `last5PinUs`, `lastPianoUs`, `lastPnoscanUs`, `lastPnoscanAdjUs`, `lastMidiOutUs` | int | last-loop microsecond timings for each subsystem (health/perf) |
| `pnoscanEraseAdj` | bool | PNOScan calibration flag |
| `cpu` | obj | `{"user": <n>|null}` CPU usage; app also reads `cpu.usage` + `load[0]` when present |

### Mutes / audio routing state

| Field | Type |
|-------|------|
| `mute_master`, `mute_piano`, `mute_voice`, `mute_mp3`, `mute_midiOut`, `mute_synthMidi`, `mute_synthGain`, `mute_dac1`, `mute_dac2`, `mute_dac3` | bool each |
| `quietMode` | bool (night/quiet play) |
| `QRSSynthLoaded` | bool (soft-synth soundfont loaded) |
| `currentVolumeSettings` | obj — per-output `{id,desc,lval,mval,hval}` (low/mid/high volume curve points). Contains the live values for master vol etc. |
| `currentAudioRoute` | array — `{AUDIO_SOURCE_ID,SOURCE,AUDIO_SINK_ID,SINK,STATE}` (e.g. "Audio In" → "Lower Left Audio", speaker matrix) |
| `currentMidiRoute` | array — `{MIDI_SOURCE_ID,SOURCE,CHANNEL,MIDI_SINK_ID,SINK,ROUTE_DELAY}`; sources/sinks include `5-Pin MIDI In/Out`, `Piano`, `Software Synthesizer`, `File`, `USB Midi Out`, `USB Device 1/2 Out`, `Bluetooth Midi Out`, `Mosquitto In/Server Out/Local Out` |
| `fileTranslationCurve` | array — file-type → translation curve (`Midi File`, `.QRS Midi File`, `MP3/AMI File`, `MP3/Midi Combo`, `MP3/.QRS Combo`) |
| `pnoscan` | array — PNOScan strip config rows |

### Download / update progress (useful "updating" sensor)

| Field | Type |
|-------|------|
| `updateInProgress` | bool |
| `downloadInProgress` | bool |
| `totalToDownload`, `totalDownloaded` | int (bytes) |
| `currentDownload`, `currentDownloaded`, `currentFileDownload` | int |
| `rsyncCurrentMedia` | int |

### Connectivity / storage / misc

| Field | Type / value |
|-------|--------------|
| `internetAccess` / `Internet` | bool |
| `networkStatus`, `wifiStatus` | int (1 = up) |
| `networkConnection` | obj `{wsEnabled,wcEnabled,ethEnabled,mac,wmac,wip,wcast,wmask,wgw,gw,dns,wdns,wapPresent}` |
| `microsd`, `sdCard`, `usbSplash`, `localVid` | bool storage presence |
| `usbCount`, `driveIndex` | USB drives attached |
| `drives` | obj — `df` output per mount: `{root:[fs,size,used,avail,use%,mount], "/tmp":[…], "/media/microsdp1":[…], …}` |
| `libraryVersion` | float (0.438) — bump ⇒ re-sync `music_stream` |
| `tagVersion` | float (0.717) — bump ⇒ re-sync `tags` |
| `btRequest` | int — pending Bluetooth pairing/connect request |
| `remoteSsh` | int — remote-support SSH tunnel state |
| `dealerInformation` | array `[{business,contact,email,account,phone}]` |
| `userInformation`, `cloudInformation` | string (empty here) |
| `index` | bool — library indexing running |

---

## Recommended HA state mapping

| HA `media_player` attribute | Source |
|---|---|
| `state` | `currentPlayerState` → `playing` / `paused` / `idle`; `off` if `currentPowerOn==false` && stopped |
| `media_position` / `media_position_updated_at` | `currentTrackProgrssMs/1000` |
| `media_duration` | `currentTrackDurationMs/1000` |
| `media_title` / `media_artist` | `tags[catalog][track]` from `filePath` (fallback: parse `getStatus.song` `"Artist - Title (path)"`) |
| `media_playlist` | `playListName` |
| `repeat` | `repeat` (0/1/2 → off/one/all) |
| `shuffle` | `shuffle` |
| `volume_level` | setting id `47` (Master Volume) / 100 |
| `is_volume_muted` | `mute_master` |
| extra sensors | `systemFaults`, `systemWarnings`, `updateInProgress`/`downloadInProgress` (+ progress %), `currentPowerOn`, `btRequest`, `quietMode`, disk free from `drives` |
