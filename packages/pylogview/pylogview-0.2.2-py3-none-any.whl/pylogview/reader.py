import typing as t

from pylogview import datefinder
from pylogview.record import LogRecord

if t.TYPE_CHECKING:
    from pylogview.window import Window


class LogReader:
    __slots__ = [
        "_window",
        "filename",
        "_lines",
        "records",
        "_record_prefix_length",
        "_fd",
        "_buffer",
    ]

    def __init__(self, window: "Window", filename: str):
        self._window = window
        self.filename = filename
        self._lines = 0  # file line count
        self.records: t.List[LogRecord] = []
        self._record_prefix_length: t.Union[
            str, None
        ] = None  # pattern that starts record
        self._fd = None
        self._buffer = bytes()  # byte buffer for file data
        self._open()

    def __del__(self):
        if self._fd:
            try:
                self._fd.close()
            except:
                pass

    @property
    def isOpen(self) -> bool:
        if self._fd is not None:
            return not self._fd.closed
        return False

    @property
    def lines(self) -> int:
        return self._lines

    def preload(self) -> t.List[LogRecord]:
        self._get_line_count()
        self._read_last()
        return self.read(0)

    def read(self, records: int = 1) -> t.List[LogRecord]:
        """Read to end of file and parse next line"""
        self._read()
        return self._get_records(records)

    ##### Internal Methods #####

    def _open(self):
        try:
            self._fd = open(self.filename, "rb")
        except IOError as err:
            self._window.log.append(
                f"Failed to open '{self.filename}': [{err.errno}] {err.strerror}"
            )
            self._fd = None

    def _read(self):
        if self.isOpen:
            try:
                data = self._fd.read()
                self._lines += data.count(b"\n")
                self._buffer += data
            except IOError as err:
                self._window.log.append(
                    f"Error while reading '{self.filename}': [{err.errno}] {err.strerror}"
                )

    def _get_line_count(self):
        if not self.isOpen:
            return
        try:
            self._fd.seek(0, 0)
            self._lines = 0
            for line in self._fd:  # pylint: disable=unused-variable
                self._lines += 1
        except IOError as err:
            self._fd = None
            self._lines = 0
            self._window.log.append(
                f"Error while reading '{self.filename}': [{err.errno}] {err.strerror}"
            )

    def _read_last(self):
        """Read last ``lines`` of file, like 'tail -n'"""
        if not self.isOpen:
            return
        try:
            last_read_block = self._fd.tell()
            block_end_byte = last_read_block
            BLOCK_SIZE = min(block_end_byte, 1024)
            remain_lines = self._window.config.lines
            block_num = -1
            blocks = []
            while remain_lines > 0 and block_end_byte > 0:
                if block_end_byte - BLOCK_SIZE > 0:
                    self._fd.seek(block_num * BLOCK_SIZE, 2)
                    blocks.append(self._fd.read(BLOCK_SIZE))
                else:
                    self._fd.seek(0, 0)
                    blocks.append(self._fd.read(block_end_byte))
                remain_lines -= blocks[-1].count(b"\n")
                block_end_byte -= BLOCK_SIZE
                block_num -= 1
            self._fd.seek(last_read_block, 0)
        except IOError as err:
            self._fd = None
            self._window.log.append(
                f"Error while reading '{self.filename}': [{err.errno}] {err.strerror}"
            )
        else:
            for block in blocks[::-1]:
                self._buffer += block

    def _find_record_prefix_length(self):
        """
        Rudamentary prefix length finder. Looks for repeated same number of chars
        between newline/file-start and timestamp.
        """
        prefix_lengths = []
        last_end = 1
        buffer_string = self._buffer.decode()
        for result in datefinder.find_dates(buffer_string, source=True, index=True):
            if self._record_prefix_length is not None:
                break
            elif len(result[1]) < 6:
                # skip matches too short, probably just numbers not a timestamp
                continue
            timestamp_end = result[2][1]
            timestamp_start = timestamp_end - len(result[1]) - 1
            prefix_lengths.append(
                len(
                    buffer_string[
                        timestamp_start
                        - buffer_string[last_end:timestamp_start][::-1].find(
                            "\n"
                        ) : timestamp_start
                    ]
                )
            )
            last_end = buffer_string.find("\n", timestamp_end)
            for length in prefix_lengths:
                if prefix_lengths.count(length) > 3:
                    self._record_prefix_length = length
                    break

    def _get_records(self, count) -> t.List[LogRecord]:
        # make sure we have a lock on the prefix before parsing anything
        if self._record_prefix_length is None:
            self._find_record_prefix_length()
            if self._record_prefix_length is None:
                return []

        # find timestamps in buffer
        buffer_string = self._buffer.decode()
        timestamp_match = datefinder.find_dates(buffer_string, source=True, index=True)
        this_result = next(timestamp_match, None)
        match_offset = 0
        new_records = 0
        while True:
            if len(self._buffer) == 0:
                break

            if this_result is None:
                # if no timestamps found, read to the end of the buffer
                this_start = len(self._buffer)
            else:
                # skip if this match is too short, sometimes numbers will match
                if len(this_result[1]) < 8:
                    this_result = next(timestamp_match, None)
                    continue
                # this should always work out to 0, anything else means there is
                # data in the buffer that belongs to the previous record
                this_start = (
                    this_result[2][1]
                    - match_offset
                    - len(this_result[1])
                    - 1
                    - self._record_prefix_length
                )

            if this_start != 0:
                # make sure this match is a record
                if this_result is not None and buffer_string[this_start - 1] != "\n":
                    this_result = next(timestamp_match, None)
                    continue
                # something left in the buffer before the this record start
                # append it to the last record and search again
                if self.records:
                    # only keep if there is at least one record, anything else is
                    # a partial record from tail-ing the file
                    self.records[-1].append(buffer_string[:this_start].split("\n"))
                self._buffer = self._buffer[len(buffer_string[:this_start].encode()) :]
                buffer_string = buffer_string[this_start:]
                match_offset += this_start
                this_start -= match_offset

            while True:
                next_result = next(timestamp_match, None)
                if next_result is None:
                    # no second timestamp found, read to the end of the buffer
                    next_start = len(self._buffer)
                else:
                    # if len(next_result[1]) < 8:
                    #    continue
                    next_start = (
                        next_result[2][1]
                        - match_offset
                        - len(next_result[1])
                        - 1
                        - self._record_prefix_length
                    )
                if next_result is None or buffer_string[next_start - 1] == "\n":
                    self.records.append(
                        LogRecord(
                            self._window,
                            buffer_string[:next_start].split("\n"),
                        )
                    )
                    self._buffer = self._buffer[
                        len(buffer_string[:next_start].encode()) :
                    ]
                    buffer_string = buffer_string[next_start:]
                    match_offset += next_start
                    new_records += 1
                    break

            if next_result is None or new_records == count:
                break
            else:
                this_result = next_result

        self.records = self.records[0 - self._window.config.lines :]
        return self.records[0 - new_records :] if new_records else []
