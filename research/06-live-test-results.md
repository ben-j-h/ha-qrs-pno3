# Live Test Results — write path

Tested against the real piano on 2026-09-05. Test song: musicId **2489** / libraryId **1** = *Barnabas Fekete – "1900 Love Song"* (`/media/microsdp1/801341/01.qrs`, catalog 801341 track 1, "Romance And More", genre "Dinner Music - Solo Piano").

Helper script: [`probe/pno.py`](probe/pno.py).

## ✅ Verified working

| Command | Request | Observed |
|---|---|---|
| **Play song** | `changePlaySettingsJSON.php?requestType=setPlayMode&playSource=F&state=1&libraryId=1&songId=2489&restart=1` | `{"success":true,"state":"1"}`. Rails powered on automatically, `currentPlayerState→1`, `currentTrackProgrssMs` advances in real time, `currentTrackDurationMs=107528`. `currentPlaylistType` flips `3→0` (single-file mode), `currentPlaylistTrackId` becomes the musicId. |
| **Pause** | `…requestType=setPlayMode&state=2` | `{"success":true,"state":"2"}`. `currentPlayerState→2`, position frozen across polls. |
| **Resume** | `…requestType=setPlayMode&state=1` | Continues from the paused position (no restart). |
| **Stop** | `…requestType=setPlayMode&state=0` | `currentPlayerState→0`, `currentTrackProgrssMs→0`. |
| **Seek** | `…requestType=sendCommand&msg=<chk>` where cmd `$|<ms>` | `{"success":true,"sentMsg":"282|$|60000"}`. Position jumped to the target. **Checksum confirmed** = decimal sum of `ord(c)` for every char except `|`, formatted `"<sum>|<cmd>"` (leading `|` ensured). |
| **Master volume** | `changeSettingsJSON.php?requestType=setParam&param=47&val=<0-100>` | `{"success":true,"val":"45","sync":true}`. Confirmed by re-reading `all_stream.php?js` (`qrs.vals` id 47). Restored to 50. |
| **Repeat** | `changePlaySettingsJSON.php?requestType=setRepeat&val=<0|1|2>` | `{"success":true,"val":2}`. Reflected in `playbackInformation.repeat`. |
| **Shuffle** | `changePlaySettingsJSON.php?requestType=setShuffle&val=<0|1>` | `{"success":true,"val":1}`. Reflected in `playbackInformation.shuffle`. |
| **Status (title)** | `changePlaySettingsJSON.php?requestType=getStatus` | `{"song":"Barnabas Fekete - 1900 Love Song (/media/microsdp1/801341/01.qrs)","state":1,"power":1,"faults":0,"warnings":0}`. NOTE: top-level `"success":false,"message":"Failed to Update!"` is **noise** — the real fields are valid. |
| **State poll** | `all_stream.php?quick=1&settings=<hi>&…` | ~0.25 s, full `playbackInformation`. Best poll source. |

## ⚠️ Partial / quirks

| Thing | Finding |
|---|---|
| **Tempo / transpose** (`param=10000` / `10002`) | `setParam` returns `{"success":true,"val":"20","sync":true}` **but no observed runtime effect** — `playbackInformation.tempo`/`transpose` stayed `0` and `currentTrackDurationMs` did not change, both while stopped and mid-playback. The web app slider may use `setQuickParam` or a `sendCommand` opcode, or these need "lock" (`I|1|10001`) first. **Recommendation: expose tempo/transpose read-only in v1**, revisit the write path later. |
| **`setPower&powerOn=0`** | Returns `{"success":true,"powerOn":"0"}` but `currentPowerOn` stays `true` for minutes afterward. The PNO3 keeps the solenoid rail supply up and drops it on its own idle timer. `powerOn=1` (and implicit power-on when a song starts) works immediately. **`turn_off` = stop + best-effort `powerOn=0`; just mirror `currentPowerOn`.** |
| **Next / previous track** | No server-side command. `sendCommand("N")` returns success but does nothing. `sendCommand("V")` restarts the current track (verified earlier: forces position negative → track restarts). The web app advances tracks **client-side** (picks the next `songId` and issues the play form). **Integration must implement next/prev by walking the active playlist/library order itself.** |
| `getStatus` envelope | Always `"success":false,"message":"Failed to Update!"` even when the payload is fine — do not gate on it. |
| `all_stream` settings deltas | Do **not** include volume-curve params (id 47 etc.) even with `settings=0`. Read those from `all_stream.php?js` (`qrs.vals`, 289 KB, current values in `val`) on a slow cadence + optimistic update on our own writes. |

## Net conclusion

Core transport + volume + repeat/shuffle + seek are solid and fast. Enough to build a real `media_player`. Tempo/transpose and hard power-off are cosmetic gaps documented above.
