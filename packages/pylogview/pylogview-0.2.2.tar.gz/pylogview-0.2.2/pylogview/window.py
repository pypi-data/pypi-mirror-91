__all__ = ["Window"]

import locale
import os
import typing as t

from pylogview.common import (
    ACTIVE_DELAY,
    BLK,
    BLK_B,
    BLK_BL,
    BLK_BR,
    BLK_L,
    BLK_R,
    COLORS,
    LOG_BG,
    WIN_FRAME,
    WIN_FRAME_ACTIVE,
    WIN_FRAME_ERROR,
    WIN_FRAME_LOAD,
    WIN_FRAME_SELECT,
    WIN_FRAME_SELECT_ACTIVE,
    WIN_LINES,
    WIN_TITLE,
    tformat,
    tprint,
)
from pylogview.reader import LogReader

if t.TYPE_CHECKING:
    from pylogview.record import LogRecord


class Window(object):
    __slots__ = [
        "config",
        "log",
        "colors",
        "name",
        "term",
        "_selected",
        "active_delay",
        "reader",
        "_display_lines",
        "_last_line",
        "frame",
        "x",
        "y",
        "w",
        "h",
    ]

    def __init__(self, filename, config, log):
        self.config = config
        self.log = log
        self.colors = []
        self.name = os.path.split(filename)[-1]
        self.term = None
        self._selected = False
        self.active_delay = 0
        self.reader = LogReader(self, filename)
        self._display_lines = []
        self._last_line = 0
        self.frame = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        if value:
            self.frame = self.colors[
                WIN_FRAME_SELECT_ACTIVE if self.active_delay else WIN_FRAME_SELECT
            ]
        else:
            self.frame = self.colors[
                WIN_FRAME_ACTIVE if self.active_delay else WIN_FRAME
            ]

    def start(self, term):
        self.term = term
        self.colors.extend(COLORS[term.number_of_colors])
        self.frame = self.colors[WIN_FRAME_LOAD]
        self.draw_frame(True)

    def load(self):
        self.reader.preload()
        self._update_display_lines()
        if self.reader.isOpen:
            self.frame = self.colors[WIN_FRAME_SELECT if self.selected else WIN_FRAME]
        else:
            self.frame = self.colors[WIN_FRAME_ERROR]

    def resize(self, x, y, w, h, update):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if update:
            self._update_display_lines()
            self.refresh(True)

    def refresh(self, force=False):
        new_records = self.reader.read(0)
        if new_records and not force:
            self.active_delay = ACTIVE_DELAY
            self.frame = self.colors[
                WIN_FRAME_SELECT_ACTIVE if self._selected else WIN_FRAME_ACTIVE
            ]
            self._update_display_lines(new_records)

        if new_records or force:
            self.draw_frame()
            tformat(self.term.on_color(self.colors[LOG_BG]))
            for i in range(self.h - 2):
                print(
                    self.term.move(self.y + (self.h - 2 - i), self.x + 1)
                    + (" " * (self.w - 2))
                    + self.term.move(self.y + (self.h - 2 - i), self.x + 1)
                    + (
                        self._display_lines[
                            len(self._display_lines) + self._last_line - i - 1
                        ]
                        if len(self._display_lines) + self._last_line - i - 1 >= 0
                        else (" " * (self.w - 2))
                    )
                )

        if self._last_line == 0 and not new_records:
            if self.active_delay > 0:
                self.active_delay -= 1
            else:
                new_frame = self.colors[
                    WIN_FRAME_SELECT if self._selected else WIN_FRAME
                ]
                if self.frame != new_frame:
                    self.frame = new_frame
                    self.draw_frame()
                else:
                    self.frame = new_frame

    def scroll_up(self, lines=1):
        if len(self._display_lines) < self.h - 2:
            return
        max_scroll = 0 - len(self._display_lines) + 1 + (self.h - 2)
        if self._last_line > max_scroll:
            self._last_line -= lines
        if self._last_line < max_scroll:
            self._last_line = max_scroll

    def scroll_down(self, lines=1):
        if self._last_line < 0:
            self._last_line += lines
        if self._last_line > 0:
            self._last_line = 0

    def scroll_end(self):
        self._last_line = 0

    def page_up(self):
        self.scroll_up(self.h - 2)

    def page_down(self):
        self.scroll_down(self.h - 2)

    def draw_frame(self, fill=False):
        tprint(  # draw top edge and corners
            self.term,
            self.term.move(self.y, self.x),
            self.term.color(self.frame) + self.term.on_color(self.colors[LOG_BG]),
            BLK * int((self.w - len(self.name)) / 2),
            self.term.color(self.colors[WIN_TITLE]) + self.term.on_color(self.frame),
            self.term.bold,
            self.name,
            self.term.color(self.frame) + self.term.on_color(self.colors[LOG_BG]),
            BLK
            * int(
                (
                    ((self.w - len(self.name)) / 2)
                    + (((self.w - len(self.name)) / 2) % 1)
                )
                - 18
            ),
            self.term.color(self.colors[WIN_LINES]),
            self.term.on_color(self.frame),
            self.term.bold,
            f"lines: {locale.format_string('%d', self.reader.lines, True):>9}",
            self.term.color(self.frame) + self.term.on_color(self.colors[LOG_BG]),
            BLK * 2,
        )
        tprint(  # draw bottom edge and corners
            self.term,
            self.term.move(self.y + self.h - 1, self.x),
            self.term.color(self.frame) + self.term.on_color(self.colors[LOG_BG]),
            BLK_BL,
            BLK_B * (self.w - 2),
            BLK_BR,
        )
        # draw left and right edge and fill window
        tformat(self.term.color(self.frame) + self.term.on_color(self.colors[LOG_BG]))
        if fill:
            for row in range(self.y + 1, self.y + self.h - 1):
                print(
                    self.term.move(row, self.x) + BLK_L + (" " * (self.w - 2)) + BLK_R
                )
        else:
            for row in range(self.y + 1, self.y + self.h - 1):
                print(
                    self.term.move(row, self.x)
                    + BLK_L
                    + self.term.move(row, self.x + self.w - 1)
                    + BLK_R
                )
        # reset formatting
        tprint(self.term)

    def _update_display_lines(self, new_records: "t.List[LogRecord]" = []):
        if new_records:
            scroll_at_end = self._last_line == 0
            lines_added = 0
            for record in new_records:
                new_lines = record.display_lines
                lines_added += len(new_lines)
                self._display_lines.extend(new_lines)

            if not scroll_at_end:
                self.scroll_up(len(self._display_lines) - lines_added)
            self._display_lines[
                sum([len(record.display_lines) for record in new_records]) :
            ]
        else:
            self._display_lines = []
            for record in self.reader.records:
                self._display_lines.extend(record.display_lines)
            self._last_line = 0
