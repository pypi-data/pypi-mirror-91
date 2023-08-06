__all__ = ["LogRecord"]

import typing as t
import re
import datefinder
import textwrap
from .common import DELIMETER_PATTERNS, LOG_BG, LOG_FG, LOG_FG_DARK, LOG_LEVEL

if t.TYPE_CHECKING:
    from .window import Window


class Line:
    __slots__ = ["_text", "_format_pre", "_format_post"]

    def __init__(self, text, format_pre, format_post):
        self._text = text
        self._format_pre = format_pre
        self._format_post = format_post

    @property
    def text(self) -> str:
        return self._text

    @property
    def format_pre(self) -> str:
        return self._format_pre

    @property
    def format_post(self) -> str:
        return self._format_post

    @property
    def length(self) -> int:
        return len(self.text)

    @property
    def formatted(self) -> str:
        return self.get_formatted()[0]

    def get_formatted(self, width=0) -> t.List[str]:
        if not width or self.length <= width:
            return ["".join([self._format_pre, self._text, self._format_post])]

        return [
            "".join([self._format_pre, part, self._format_post])
            for part in textwrap.wrap(
                self._text,
                width=width,
                replace_whitespace=False,
                drop_whitespace=False,
            )
        ]


class Header(Line):
    __slots__ = ["_parts"]

    def __init__(self, window, text):
        self._parts: t.List[Line] = []
        self._parse(text, window)

    @property
    def text(self) -> str:
        return "".join([part.text for part in self._parts])

    @property
    def format_pre(self) -> str:
        return self._parts[-1]._format_pre

    @property
    def format_post(self) -> str:
        return self._parts[-1]._format_post

    def get_formatted(self, width=0) -> t.List[str]:
        if not width or self.length < width:
            return ["".join([part.formatted for part in self._parts])]

        lines = textwrap.wrap(
            self.text, width, replace_whitespace=False, drop_whitespace=False
        )
        display_lines: t.List[str] = [""] * len(lines)
        part_index = 0
        part_seek_pos = 0

        for line_index in range(len(lines)):
            line = lines[line_index]
            # if part_index==len(self._parts)-1 and not display_lines[line_index]:
            #    display_lines[line_index]="  "
            while line:
                part = self._parts[part_index]
                line_trim = 0
                if len(part.text[part_seek_pos:]) <= len(line):
                    display_lines[line_index] += (
                        f"{part._format_pre}"
                        f"{part.text[part_seek_pos:]}"
                        f"{part.format_post}"
                    )
                    line_trim = len(part.text[part_seek_pos:])
                    part_index += 1
                    part_seek_pos = 0
                else:
                    display_lines[line_index] += (
                        f"{part._format_pre}"
                        f"{part.text[part_seek_pos:part_seek_pos + len(line)]}"
                        f"{part.format_post}"
                    )
                    line_trim = len(
                        part.text[part_seek_pos : part_seek_pos + len(line)]
                    )
                    part_seek_pos += len(
                        part.text[part_seek_pos : part_seek_pos + len(line)]
                    )
                line = line[line_trim:]

        return display_lines

    def _parse(self, text, window):
        FORMAT_LOG_BG = window.term.on_color(window.colors[LOG_BG])
        FORMAT_LOG_FG = window.term.color(window.colors[LOG_FG])
        FORMAT_LOG_FG_DARK = window.term.color(window.colors[LOG_FG_DARK])

        if window.config.trim_date:
            # replace timestamp with HH:MM:SS.FFF
            timestamp_match = datefinder.find_dates(text, source=True, index=True)
            timestamp = next(timestamp_match)
            if timestamp:
                timestamp_time = timestamp[0].strftime("%H:%M:%S.%f")[:-3]
                timestamp_end = timestamp[2][1]
                timestamp_start = timestamp_end - len(timestamp[1]) - 1
                text = (
                    f"{text[:timestamp_start]}{timestamp_time}{text[timestamp_end-1:]}"
                )

        # find log level
        text_upper = text.upper()
        text_len = len(text)
        level_matches = [text_upper.find(key) for key in LOG_LEVEL.keys()]
        level_start = min(level_matches, key=lambda v: text_len if v == -1 else v)
        del text_upper, text_len
        try:
            level_key = list(LOG_LEVEL.keys())[level_matches.index(level_start)]
            level_color = window.term.color(window.colors[LOG_LEVEL[level_key]])
        except IndexError:
            level_key = ""
            level_start = 0
            level_color = window.term.color(window.colors[LOG_FG])

        # find delimiter for end of header / start of message
        delim_end = 0
        for pattern in DELIMETER_PATTERNS:
            match = re.match(pattern, text)
            if match is not None:
                delim_end = match.end() - 1
                break

        # build header
        self._parts.append(
            Line(
                text=text[:level_start],
                format_pre=f"{FORMAT_LOG_BG}{FORMAT_LOG_FG_DARK}",
                format_post=f"{FORMAT_LOG_FG}",
            )
        )
        self._parts.append(
            Line(
                text=text[level_start : level_start + len(level_key)],
                format_pre=f"{FORMAT_LOG_BG}{window.term.bold}{level_color}",
                format_post=f"{window.term.normal}{FORMAT_LOG_BG}",
            )
        )
        self._parts.append(
            Line(
                text=text[level_start + len(level_key) : delim_end],
                format_pre=f"{FORMAT_LOG_BG}{FORMAT_LOG_FG_DARK}",
                format_post=f"{FORMAT_LOG_FG}",
            )
        )

        # add remaining text
        self._parts.append(
            Line(
                text=text[delim_end:],
                format_pre=f"{FORMAT_LOG_BG}{level_color}",
                format_post=f"{FORMAT_LOG_FG}",
            )
        )


class LogRecord:
    __slots__ = ["_window", "_header", "_lines", "_width", "_display_lines"]

    def __init__(self, window: "Window", lines: t.List[str]):
        self._window = window
        self._lines: t.List[Line] = []
        self._width = 0
        self._display_lines: t.List[str] = []

        if not lines[-1]:
            # trim blank last line, this is from the pattern matcher
            lines = lines[:-1]
        self._lines.append(Header(window, lines[0]))
        lines.pop(0)
        for line in lines:
            self._lines.append(
                Line(line, self._lines[0].format_pre, self._lines[0].format_post)
            )

        self._update_display_lines()

    @property
    def display_lines(self) -> t.List[str]:
        """Return a list of strings with format codes, wrapped for the window """
        if self._width != self._window.w - 2:
            self._update_display_lines()
        return self._display_lines

    def append(self, lines: t.List[str]):
        """Add more lines to this record"""
        for line in lines:
            self._lines.append(
                Line(
                    text=line,
                    format_pre=self._lines[-1].format_pre,
                    format_post=self._lines[-1].format_post,
                )
            )
        self._update_display_lines()

    ##### Internal Methods #####

    def _update_display_lines(self):
        width = self._window.w - 2
        self._width = width
        self._display_lines: t.List[str] = []
        for line in self._lines:
            self._display_lines.extend(line.get_formatted(width))
