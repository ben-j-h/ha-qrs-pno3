# Changelog

All notable changes to this integration are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## [0.2.1] - 2026-09-05

### Fixed
- `async_setup_entry` crashed with `FileExistsError` when the
  `.storage/qrs_pno3` directory already existed (i.e. removing and re-adding
  the integration, or a second config entry). The redundant `os.makedirs` call
  passed `True` as `mode` instead of `exist_ok`; directory creation is now left
  to the library layer, which does it correctly.

## [0.2.0] - 2026-09-05

Clean tag that folds in the CI configuration landed after `v0.1.0`; no
integration code changes.

- CI: scope `ruff` to `custom_components/qrs_pno3`; ignore the HACS `brands`
  check (no `home-assistant/brands` entry yet — not required for
  custom-repository installs).
- `ruff.toml`: exclude `research/` (reverse-engineering notes + probe scripts).

## [0.1.0] - 2026-09-05

Initial release.

- `media_player` entity: play / pause / resume / stop / seek, next / previous,
  volume, mute, repeat, shuffle, turn on/off, browse & play by
  playlist / artist / album / genre, `play_media` by musicId or search text.
- Local SQLite mirror of the on-piano catalog (~14k songs) + metadata +
  playlists, built from `music_stream.php` / `tags.php` / `playlist.php` and
  auto-synced when the controller bumps `libraryVersion` / `tagVersion`.
  Independent of Home Assistant's recorder backend.
- Services: `refresh_library`, `play_song`, `send_command`,
  `set_tempo` / `set_transpose` (experimental), `clear_faults`.
- Diagnostic sensors (faults, warnings, library/tag version, song count,
  download progress), rail-power switch, clear-faults / panic-stop /
  refresh-cache buttons, disabled-by-default tempo/transpose numbers.
- Adaptive local polling (~2 s playing, ~30 s idle), config + options flow,
  diagnostics, per-entry cache cleanup on removal.

### Known limitations
- Tempo / transpose writes are accepted by the controller but have no observed
  runtime effect (exposed read-only).
- `turn_off` is best-effort: the controller de-energises the solenoid rails on
  its own idle timer.
- Next / previous is implemented client-side (no server-side command).
