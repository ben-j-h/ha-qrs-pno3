# QRS PNO3 Player Piano

Local control of a QRS PNOmation³ / PNO3 player-piano controller from Home Assistant.

- `media_player` with browse & play across the full on-piano library
- Local SQLite cache of the ~14k-song catalog, auto-synced, with a
  `qrs_pno3.refresh_library` service + button to force a rebuild
- Faults / version / download sensors, rail-power switch, clear-faults & panic-stop buttons
- Adaptive local polling, no cloud, no QRS account

Add the integration from **Settings → Devices & Services** and enter the
controller's LAN IP address.

See the repository README for options, services and known caveats
(tempo/transpose writes, power-off timing, next/previous behaviour).
