"""Constants for the QRS PNO3 integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "qrs_pno3"

MANUFACTURER: Final = "QRS Music"
MODEL: Final = "PNOmation III (PNO3)"

# --- config / options ---------------------------------------------------------
CONF_HOST: Final = "host"

OPT_IDLE_INTERVAL: Final = "idle_poll_interval"
OPT_PLAYING_INTERVAL: Final = "playing_poll_interval"
OPT_PARAMS_INTERVAL: Final = "params_refresh_interval"
OPT_TURN_OFF_STOPS: Final = "turn_off_stops_playback"

DEFAULT_IDLE_INTERVAL: Final = 30
DEFAULT_PLAYING_INTERVAL: Final = 2
DEFAULT_PARAMS_INTERVAL: Final = 60
DEFAULT_TURN_OFF_STOPS: Final = True

# --- controller parameter ids (see research/settings_dictionary.md) ----------
PARAM_MASTER_VOLUME: Final = 47
PARAM_PIANO_VOLUME: Final = 31
PARAM_TEMPO: Final = 10000
PARAM_TEMPO_PERSIST: Final = 10001
PARAM_TRANSPOSE: Final = 10002
PARAM_TRANSPOSE_PERSIST: Final = 10003

TEMPO_MIN: Final = -100
TEMPO_MAX: Final = 100
TRANSPOSE_MIN: Final = -24
TRANSPOSE_MAX: Final = 24

# --- playbackInformation.currentPlayerState ---------------------------------
STATE_STOPPED: Final = 0
STATE_PLAYING: Final = 1
STATE_PAUSED: Final = 2

# --- services ---------------------------------------------------------------
SERVICE_REFRESH_LIBRARY: Final = "refresh_library"
SERVICE_PLAY_SONG: Final = "play_song"
SERVICE_SEND_COMMAND: Final = "send_command"
SERVICE_SET_TEMPO: Final = "set_tempo"
SERVICE_SET_TRANSPOSE: Final = "set_transpose"
SERVICE_CLEAR_FAULTS: Final = "clear_faults"

ATTR_ENTRY_ID: Final = "entry_id"
ATTR_MUSIC_ID: Final = "music_id"
ATTR_QUERY: Final = "query"
ATTR_COMMAND: Final = "command"
ATTR_APPLY_CHECKSUM: Final = "apply_checksum"
ATTR_VALUE: Final = "value"

# storage
STORAGE_SUBDIR: Final = "qrs_pno3"
