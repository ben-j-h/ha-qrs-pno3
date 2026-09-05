# Control Commands

Two response flavours of the same backend:

* `GET /php/changePlaySettings.php?…` → XML `<response><success>true</success>…</response>`
* `GET /php/changePlaySettingsJSON.php?…` → JSON `{"success":…, …}` ← **prefer this for middleware/HA**

Everything is idempotent-ish HTTP GET with query params. **No auth.** The app fires these with `disableCaching` and often a `date=<epoch>` cache-buster; add `&date=<ms>` if a caching proxy is in the path.

Legend: ⚠️ = physically actuates the piano / rails.

---

## Transport

| Action | Request |
|---|---|
| **Play a specific library song** ⚠️ | `changePlaySettings.php?requestType=setPlayMode&playSource=F&state=1&libraryId=<lid>&songId=<musicId>&restart=1` |
| **Play / resume** ⚠️ | `changePlaySettings.php?requestType=setPlayMode&state=1` |
| **Pause** | `changePlaySettings.php?requestType=setPlayMode&state=2` |
| **Stop** | `changePlaySettings.php?requestType=setPlayMode&state=0` |
| **Play the current "stream"/radio source** ⚠️ | `changePlaySettings.php?requestType=setPlayMode&state=1&playSource=S` |
| **Seek to position** | `sendCommand("$|<ms>")` → `changePlaySettings.php?requestType=sendCommand&msg=<chk>|$|<ms>` |
| **Previous / restart current** ⚠️ | `sendCommand("V")` |
| **Next track** ⚠️ | play next `songId` yourself from the cached playlist, **or** `sendCommand("S__Q|P|F|1|<musicId>")` (stop + queue) |
| **Rail power on/off** ⚠️(on) | `changePlaySettings.php?requestType=setPower&powerOn=<0|1>` |
| **Clear faults** | `changePlaySettings.php?requestType=clrFaults` |
| **Repeat** | `changePlaySettings.php?requestType=setRepeat&val=<0|1|2>` (0 off / 1 one / 2 all) |
| **Shuffle** | `changePlaySettings.php?requestType=setShuffle&val=<0|1>` |
| **Status** | `changePlaySettingsJSON.php?requestType=getStatus` |

`playSource` values seen: `F` = File (library), `S` = Stream/system (radio / current), also used in the pipe language as the 2nd field.

### Playing from a playlist (as the web app does it)

The app builds a `sendCommand` batch (`__`-separated sub-commands, each checksum-prefixed) and posts it with `songPlay=true` (and `shuffleMe=true` when shuffle is on):

```
GET /php/changePlaySettings.php?songPlay=true&requestType=sendCommand&msg=<encoded batch>
```

Sub-command templates from `qrs.List2(kind, trackIndex, record)`:

| kind | raw message (before checksum) | meaning |
|---|---|---|
| `main` | *(not sendCommand)* `requestType=setPlayMode&playSource=F&state=1&libraryId=<lid>&songId=<id>&restart=1` | play one song by id |
| `temp` | `S__P|F|1|<playlistId>|<trackIndex>` | stop, then play playlist type 1 (temp) at index |
| `persist` | `P|F|2|-3|0__S__P|F|2|<playlistId>|<trackIndex>` | set persistent playlist type 2, then play it at index |
| `stream` | *(not sendCommand)* `requestType=setPlayMode&state=1&playSource=S` | play current stream |

For an integration it's simplest to **ignore the pipe language for playlists** and just: look up the playlist's track list from the cache → play each `songId` via the plain `main` form, advancing on `currentPlayerState==0`.

---

## The `sendCommand` pipe mini-language

Helper in the app:

```js
function sendCommand(cmd) {
  // split on "__" into sub-commands; for each:
  //   sum = Σ charCodeAt(c) for every char that isn't "|"
  //   ensure it starts with "|"
  //   prefix the sum:  msg = sum + "|" + rest      e.g. "V" -> "86|V", "$|1234" -> checksum + "|$|1234"
  // rejoin sub-commands with "__", URL-encode
  // GET ../php/changePlaySettings.php?requestType=sendCommand&msg=<result>
}
```

Checksum = **decimal sum of the ASCII codes of all non-`|` characters** in that sub-command, prepended followed by `|`. Sub-commands joined by `__`.

Opcodes observed:

| Opcode | Form | Meaning |
|---|---|---|
| `P` | `P\|<src>\|<type>\|<playlistId>\|<track>` | Play. `src` = `F` (file). `type`: 1 = temp playlist, 2 = persistent playlist |
| `S` | `S` | Stop |
| `Q` | `Q\|P\|F\|1\|<musicId>` | Queue / cue next |
| `V` | `V` | Back / restart current track |
| `$` | `$\|<ms>` | Seek to millisecond position |
| `I` | `I\|<0\|1>\|<settingId>` | Set an integer/lock flag. Used for **Lock Tempo** (`I\|1\|10001`) and **Lock Transpose** (`I\|1\|10003`) |

Example: Lock Tempo on → sub-command `I|1|10001`
→ checksum = `73+49+49+48+48+48+49` (chars `I 1 1 0 0 0 1`, `|` excluded) = `364`
→ msg = `364|I|1|10001`
→ `GET /php/changePlaySettings.php?requestType=sendCommand&msg=364%7CI%7C1%7C10001`

*(Verify the exact checksum convention live before relying on `sendCommand`; the plain `requestType=` calls above don't need it and cover all normal control.)*

---

## Volume / tempo / transpose / EQ  (via `changeSettingsJSON.php`)

The app's sliders write with:

```
GET /php/changeSettingsJSON.php?requestType=setParam&param=<id>&val=<v>
    (some params use requestType=setQuickParam — for these ids setParam works too / is what the sliders send)
```

| Control | `param` id | Range (from `setSlider(...)`) | Notes |
|---|---:|---|---|
| **Master Volume** | `47` | `1..100` | ← `media_player.volume_level` × 100 |
| Audio Offset | `77` | `-99..100` | curve difference; `-100` = "Audio Muted" |
| Piano Offset | `78` | `-99..100` | `-100` = "Piano Muted" |
| **Tempo** | `10000` | `-100..100` (percent) | `playbackInformation.tempo`; app shows BPM via `calculateBMS` |
| **Transpose** | `10002` | `-24..24` (semitones) | `playbackInformation.transpose` |
| Bass | `48` | `-24..12` | EQ |
| Mid | `49` | `-24..12` | EQ |
| Treble | `50` | `-24..12` | EQ |
| Piano Volume | `31` | `0-100` | (from settings dict) |
| Soft Volume | `24` | `0-100` | |
| Dynamic Volume | `25` | `0-100` | |
| Lock Tempo | `10001` | `0/1` | set via `sendCommand("I|<0|1>|10001")` |
| Lock Transpose | `10003` | `0/1` | set via `sendCommand("I|<0|1>|10003")` |

Response (JSON variant) echoes `{"success":true,"val":"<applied>"}`-ish; XML variant returns `<success>true</success><val>…</val>`.

> There are **1,222** settable params total — see [`settings_dictionary.md`](settings_dictionary.md). The vast majority are solenoid/pedal calibration, MIDI routing, and DAC curves that an integration should **not** touch. Stick to the table above.

Per-channel mix: `GET /php/changeModulation.php?id=<n>` reads, `?id=<n>&value=<v>` writes (the "modulation volumes" popup).

---

## Things to avoid from an integration

| Endpoint | Why |
|---|---|
| `netApply.php`, `bootApply.php`, `wifi/*` | reconfigures networking / can drop the box off the LAN |
| `changeSettings.php?requestType=killAll` | hard-stops all solenoid output (ok as a panic-stop, but disruptive) |
| `setClock.php` | changes RTC |
| `delete.php`, `fileUsb.php`, `pnoCloud*` | mutate/delete library content |
| `setRoutesTable`, `setAudioRouterAll`, `setCurve`, `setDacCurves`, `setNote`, `setPedal` | calibration / routing — wrong values can make the piano play badly or not at all |

---

## Minimal control surface for HA (recommended)

| HA service | Call |
|---|---|
| `media_player.play_media` (id = musicId) | `setPlayMode&playSource=F&state=1&libraryId=<lid>&songId=<id>&restart=1` |
| `media_player.media_play` | `setPlayMode&state=1` |
| `media_player.media_pause` | `setPlayMode&state=2` |
| `media_player.media_stop` | `setPlayMode&state=0` |
| `media_player.media_seek` | `sendCommand $|<ms>` |
| `media_player.media_next_track` | advance musicId from cached playlist → play form |
| `media_player.media_previous_track` | `sendCommand V` (or previous musicId) |
| `media_player.volume_set` | `changeSettingsJSON setParam param=47 val=<0-100>` |
| `media_player.volume_mute` | `changeSettingsJSON` mute route, or `param=47 val=1` / restore |
| `media_player.repeat_set` | `setRepeat val=<0/1/2>` |
| `media_player.shuffle_set` | `setShuffle val=<0/1>` |
| `media_player.turn_on` / `turn_off` | `setPower powerOn=<1/0>` |
| `switch`/`number` helpers | tempo (`10000`), transpose (`10002`), quiet mode, clear-faults button |
