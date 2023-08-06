DELIMETER_PATTERNS = [r".*( \| )", r".*( - )", r".*(\] [^\[])"]

MAX_COLS = 3
MAX_ROWS = 4
MAX_WINS = MAX_COLS * MAX_ROWS
ACTIVE_DELAY = 10
LOOP_MS = 50

BLK_T = "\u2580"
BLK_B = "\u2584"
BLK = "\u2588"
BLK_L = "\u258C"
BLK_R = "\u2590"
BLK_BL = "\u2599"
BLK_TL = "\u259B"
BLK_TR = "\u259C"
BLK_BR = "\u259F"

APP_FG = 0
APP_BG = 1
APP_FRAME = 2
APP_TITLE = 3
APP_CLOCK = 4
WIN_FRAME = 5
WIN_FRAME_ACTIVE = 6
WIN_FRAME_SELECT = 7
WIN_FRAME_SELECT_ACTIVE = 8
WIN_FRAME_LOAD = 9
WIN_FRAME_ERROR = 10
WIN_TITLE = 11
WIN_LINES = 12
LOG_FG = 13
LOG_FG_DARK = 14
LOG_BG = 15
LOG_LEVEL = {
    "TRACE": 16,
    "DEBUG": 17,
    "INFO": 18,
    "WARNING": 19,
    "WARN": 19,
    "ERROR": 20,
    "CRITICAL": 21,
    "EMERG": 21,
}
# fmt: off
COLORS = {
    16: [
        15, # APP_FG
        16, # APP_BG
        4,  # APP_FRAME
        3,  # APP_TITLE
        16, # APP_CLOCK
        2,  # WIN_FRAME
        10, # WIN_FRAME_ACTIVE
        6,  # WIN_FRAME_SELECT
        14, # WIN_FRAME_SELECT_ACTIVE
        3,  # WIN_FRAME_LOAD
        1,  # WIN_FRAME_ERROR
        16, # WIN_TITLE
        16, # WIN_LINES
        15, # LOG_FG
        8,  # LOG_FG_DARK
        16, # LOG_BG
        8,  # LOG_LEVEL: TRACE
        8,  # LOG_LEVEL: DEBUG
        10, # LOG_LEVEL: INFO
        11, # LOG_LEVEL: WARN
        9,  # LOG_LEVEL: ERROR
        1,  # LOG_LEVEL: CRITICAL
    ],
    88: [
        15, # APP_FG
        16, # APP_BG
        4,  # APP_FRAME
        3,  # APP_TITLE
        16, # APP_CLOCK
        28, # WIN_FRAME
        46, # WIN_FRAME_ACTIVE
        6,  # WIN_FRAME_SELECT
        45, # WIN_FRAME_SELECT_ACTIVE
        3,  # WIN_FRAME_LOAD
        1,  # WIN_FRAME_ERROR
        16, # WIN_TITLE
        16, # WIN_LINES
        15, # LOG_FG
        8,  # LOG_FG_DARK
        16, # LOG_BG
        8,  # LOG_LEVEL: TRACE
        8,  # LOG_LEVEL: DEBUG
        40, # LOG_LEVEL: INFO
        11, # LOG_LEVEL: WARN
        9,  # LOG_LEVEL: ERROR
        52, # LOG_LEVEL: CRITICAL
    ],
    256: [
        15, # APP_FG
        16, # APP_BG
        4,  # APP_FRAME
        3,  # APP_TITLE
        16, # APP_CLOCK
        28, # WIN_FRAME
        46, # WIN_FRAME_ACTIVE
        6,  # WIN_FRAME_SELECT
        45, # WIN_FRAME_SELECT_ACTIVE
        3,  # WIN_FRAME_LOAD
        1,  # WIN_FRAME_ERROR
        16, # WIN_TITLE
        16, # WIN_LINES
        15, # LOG_FG
        240,# LOG_FG_DARK
        233,# LOG_BG
        242,# LOG_LEVEL: TRACE
        246,# LOG_LEVEL: DEBUG
        40, # LOG_LEVEL: INFO
        208,# LOG_LEVEL: WARN
        9,  # LOG_LEVEL: ERROR
        124,# LOG_LEVEL: CRITICAL
    ]
}
# fmt: on


def tprint(term, *s):
    if len(s) == 0:
        print(term.move(0, 0) + term.normal)
    else:
        print(*s, sep="", end=term.normal)


def tformat(*s):
    print(sep="", end="".join(s))
