#!/usr/bin/env python3
"""Tiny manual test client for the QRS PNO3. Read-heavy; writes only when told."""
import json, sys, time, urllib.parse, urllib.request

HOST = "192.168.0.225"
BASE = f"http://{HOST}/php"


def _get(path):
    url = f"{BASE}/{path}"
    with urllib.request.urlopen(url, timeout=12) as r:
        return r.read().decode("utf-8", "replace")


def state():
    raw = _get("all_stream.php?quick=1&settings=99999999&state=0&fullCount=99999999&demoCount=99999999&tempCount=99999999&date=%d" % (time.time() * 1000))
    arr = json.loads(raw)
    deltas = {e["id"]: e["val"] for e in arr if isinstance(e, dict) and e.get("id", 0) >= 0}
    pb = next(e["playbackInformation"] for e in arr if isinstance(e, dict) and e.get("id") == -1)
    return pb, deltas


KEYS = ["currentPlayerState", "currentStatus", "currentPowerOn", "currentMusicId",
        "currentLibraryId", "currentPlaylistType", "currentPlaylistId",
        "currentPlaylistTrackId", "currentTrackProgrssMs", "currentTrackDurationMs",
        "repeat", "shuffle", "tempo", "transpose", "systemFaults", "systemWarnings",
        "mute_master", "playListName", "filePath"]


def show(tag=""):
    pb, d = state()
    line = {k: pb.get(k) for k in KEYS}
    print(f"[{tag}] " + "  ".join(f"{k}={line[k]}" for k in KEYS))
    print(f"       settings-deltas: 47(vol)={d.get(47)} 10000(tempo)={d.get(10000)} 10002(transpose)={d.get(10002)}")
    return pb, d


def checksum_cmd(cmd):
    """sendCommand encoding: sum of ASCII of non-'|' chars, prefixed; sub-cmds joined by __."""
    out = []
    for part in cmd.split("__"):
        b = sum(ord(c) for c in part if c != "|")
        if not part.startswith("|"):
            part = "|" + part
        out.append(f"{b}{part}")
    return "__".join(out)


def send_raw(qs, json_variant=True):
    ep = "changePlaySettingsJSON.php" if json_variant else "changePlaySettings.php"
    print(f"  >>> GET /{ep}?{qs}")
    resp = _get(f"{ep}?{qs}")
    print(f"  <<< {resp.strip()[:400]}")
    return resp


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if cmd == "show":
        show("now")
    elif cmd == "sendcmd":  # pno.py sendcmd 'S__P|F|1|0|3'
        print(checksum_cmd(sys.argv[2]))
    elif cmd == "raw":      # pno.py raw 'requestType=setPlayMode&state=0'
        send_raw(sys.argv[2], json_variant=(len(sys.argv) < 4 or sys.argv[3] != "xml"))
    elif cmd == "watch":    # pno.py watch 20  -> poll every 1s for N s
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        for _ in range(n):
            show(time.strftime("%H:%M:%S"))
            time.sleep(1)
