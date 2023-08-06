import argparse
import curses
import datetime
import locale
import os
import signal
import time
from concurrent import futures

import blessings

from .version import __version__
from .window import Window
from .common import (
    APP_BG,
    APP_FG,
    APP_TITLE,
    BLK,
    COLORS,
    LOOP_MS,
    MAX_WINS,
    MAX_COLS,
    APP_FRAME,
    APP_CLOCK,
    tprint,
    tformat,
)

TERM_TITLE = "logview"
APPLICATION_TITLE = f"logview v{__version__}"

locale.setlocale(locale.LC_ALL, "")

config = None
windows = []
colors = []
log = []


class Logger:
    @staticmethod
    def append(value):
        log.append(value)


class SignalHook:
    """
    Hooks to SIGINT, SIGTERM, SIGKILL
    """

    SIGINT = signal.SIGINT
    SIGTERM = signal.SIGTERM
    SIGKILL = signal.SIGKILL

    def __init__(self):
        self._last_signal = None
        try:
            signal.signal(signal.SIGINT, self._signal_received)
        except OSError:
            pass
        try:
            signal.signal(signal.SIGTERM, self._signal_received)
        except OSError:
            pass
        try:
            signal.signal(signal.SIGKILL, self._signal_received)
        except OSError:
            pass

    def _signal_received(self, signum, frame):
        self._last_signal = signal.Signals(signum)  # pylint: disable=no-member

    @property
    def signal(self):
        return self._last_signal

    @property
    def exit(self):
        return self._last_signal in [self.SIGINT, self.SIGTERM, self.SIGKILL]


def parse_args():
    parser = argparse.ArgumentParser(
        prog="logview", description="logview allows you to tail multiple files at once"
    )
    parser.add_argument(
        "-t",
        "--trim-date",
        action="store_true",
        help="display only time from timestamp",
    )
    parser.add_argument(
        "-n",
        "--lines",
        metavar="NUM",
        type=int,
        default=1000,
        help="scrollback buffer lines (default 1000)",
    )
    parser.add_argument(
        "-d",
        "--dir",
        default="",
        help="directory to find FILE(s) in",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show version number and exit",
    )
    parser.add_argument(
        "file", metavar="FILE", nargs="+", help=f"file(s) to tail, maximum {MAX_WINS}"
    )
    return parser.parse_args()


def draw_app(term):
    top_before_title = int((term.width - len(APPLICATION_TITLE)) / 2)
    top_after_title = int(
        ((term.width - len(APPLICATION_TITLE)) / 2)
        + (((term.width - len(APPLICATION_TITLE)) / 2) % 1)
        - 12  # clock space
    )
    tprint(
        term,
        term.move(0, 0),
        term.color(colors[APP_FRAME]),
        term.on_color(colors[APP_BG]),
        BLK * top_before_title,
        term.color(colors[APP_TITLE]),
        term.on_color(colors[APP_FRAME]),
        term.bold,
        APPLICATION_TITLE,
        term.color(colors[APP_FRAME]),
        term.on_color(colors[APP_BG]),
        BLK * top_after_title,
        term.color(colors[APP_CLOCK]),
        term.on_color(colors[APP_FRAME]),
        term.bold,
        datetime.datetime.now().strftime("%H:%M:%S"),
        term.color(colors[APP_FRAME]),
        term.on_color(colors[APP_BG]),
        BLK * 4,
        term.move(term.height - 1, 0),
        # BLK * term.width,
        term.color(colors[APP_CLOCK]),
        term.on_color(colors[APP_FRAME]),
        "TAB: Next Window   SPACE: Jump to end   Q: Quit".center(term.width),
    )
    tformat(term.color(colors[APP_FRAME]), term.on_color(colors[APP_BG]))
    for row in range(1, term.height - 1):
        print(term.move(row, 0) + BLK + term.move(row, term.width - 1) + BLK)
    tprint(term)


def draw_clock(term):
    tprint(
        term,
        term.move(0, term.width - 12),
        term.color(colors[APP_CLOCK]),
        term.on_color(colors[APP_FRAME]),
        term.bold,
        datetime.datetime.now().strftime("%H:%M:%S"),
    )


def calculate_windows(term, update=True):
    col_count = 1
    row_count = 1
    row_limit = 3
    while len(windows) / col_count / row_count > 1:
        if row_count == row_limit:
            row_count = 1
            row_limit += 1
            col_count += 1 if col_count < MAX_COLS else 0
        else:
            row_count += 1

    win_width = int((term.width - 2) / col_count)
    for col in range(col_count):
        col_windows = [i for i in range(len(windows))][
            row_count * col : row_count * (col + 1)
        ]
        win_height = int((term.height - 2) / len(col_windows))
        for win in col_windows:
            windows[win].resize(
                x=win_width * col + 1,
                y=win_height * col_windows.index(win) + 1,
                w=win_width,
                h=win_height,
                update=update,
            )


def main_loop(term, screen):
    sighook = SignalHook()
    selected_window = 0
    windows[selected_window].selected = True
    windows[selected_window].draw_frame()
    while not sighook.exit:
        force = False
        key_code = screen.getch()

        while key_code != curses.ERR:
            force = force or (key_code != curses.ERR)
            if key_code in [ord("q"), ord("Q")]:
                return
            elif key_code == curses.KEY_RESIZE:
                draw_app(term)
                calculate_windows(term)
            elif key_code == 9:  # TAB
                windows[selected_window].selected = False
                selected_window += 1
                if selected_window >= len(windows):
                    selected_window = 0
                windows[selected_window].selected = True
            elif key_code == curses.KEY_UP:  # also scroll up
                windows[selected_window].scroll_up()
            elif key_code == curses.KEY_PPAGE:  # PGUP
                windows[selected_window].page_up()
            elif key_code == curses.KEY_DOWN:  # also scroll down
                windows[selected_window].scroll_down()
            elif key_code == curses.KEY_NPAGE:  # PGDN
                windows[selected_window].page_down()
            elif key_code == ord(" "):
                windows[selected_window].scroll_end()
            key_code = screen.getch()

        draw_clock(term)
        for window in windows:
            window.refresh(force)
        tprint(term)
        time.sleep(LOOP_MS / 1000)


def logview():
    term = blessings.Terminal()
    if not term.is_a_tty:
        print("logview output cannot be piped, it is for display only")
    elif term.number_of_colors < 16:
        print("logview requires a terminal that supports a minimum of 16 colours")
    else:
        global config
        config = parse_args()
        print(f"\x1b]2;{TERM_TITLE}\x07", end="")
        colors.extend(COLORS[term.number_of_colors])
        for filename in config.file:
            filepath = os.path.abspath(os.path.join(config.dir, filename))
            if os.access(filepath, os.R_OK, effective_ids=True):
                windows.append(Window(filepath, config, Logger))
            elif os.access(filepath, os.F_OK, effective_ids=True):
                print(f"File '{filepath}' is not readable")
            else:
                print(f"File '{filepath}' does not exist")
            if windows and not windows[-1].reader.isOpen:
                windows.pop(len(windows) - 1)

        if windows:
            screen = None
            try:
                screen = curses.initscr()
                curses.noecho()
                curses.cbreak()
                screen.keypad(True)
                screen.nodelay(True)
                screen.getch()

                print(
                    term.enter_fullscreen
                    + term.hide_cursor
                    + term.color(colors[APP_FG])
                    + term.on_color(colors[APP_BG])
                    + term.clear
                )
                draw_app(term)
                calculate_windows(term, False)
                for window in windows:
                    window.start(term)
                    # window.load()
                    # window.refresh(True)
                with futures.ThreadPoolExecutor() as pool:
                    threads = {pool.submit(window.load): window for window in windows}
                    for future in futures.as_completed(threads):
                        threads[future].refresh(True)
                main_loop(term, screen)
            except Exception as err:
                raise err
            finally:
                tprint(term, term.exit_fullscreen + term.normal_cursor)
                curses.nocbreak()
                if screen:
                    screen.keypad(False)
                curses.echo()
                curses.endwin()
                print(*log, sep="\n")
            exit(0)
    exit(1)


if __name__ == "__main__":
    logview()
