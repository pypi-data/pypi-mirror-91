import io
from typing import *
from .scpi_transport_base import ScpiTransports
from .scpi_type_base import ScpiTypeBase


class ScpiChars(ScpiTypeBase):
    """
    Class representing IEEE488.2 Character program data (7.7.1) and response data (8.7.1)

        This functional element is used to convey parameter information best expressed mnemonically
        as a short alpha or alphanumeric string. It is useful in cases where numeric parameters are inappropriate.
    """

    def __init__(self, s: str) -> None:
        """Initializes the object from a str type"""
        super().__init__()
        self._data = s

    def __str__(self) -> str:
        return self.as_string()

    def as_string(self) -> str:
        """Returns the char data as a Python str-object"""
        return self._data

    def as_bytes(self) -> bytes:
        """Returns the char data as a Python bytes-object"""
        return self._data.encode('ascii')

    def compose(self) -> str:
        """Composes the object into a SCPI string to be used as a parameter"""
        return self._data

    @classmethod
    def parse(cls, transport: ScpiTransports) -> 'ScpiChars':
        """Parses stream data from the device and creates a `ScpiChars` object"""
        s = transport.readline()
        return ScpiChars(s)


class ScpiNumber(ScpiTypeBase):
    """
    Class representing IEEE488.2 flexible Decimal/Nondecimal numeric NRf program data (7.7.2/7.7.4) and
    NR1/NR2/NR3 response data (8.7.2/8.7.3/8.7.4)
    """

    def __init__(self, value: Union[int, float], unit: Optional[str] = None):
        """Initializes the object from either an int (NR1) or float (NR2/NR3) value with an optional unit string"""
        super().__init__()
        self._value = value
        self._unit = unit

    def __int__(self) -> int:
        return self.as_int()

    def __float__(self) -> float:
        return self.as_float()

    def __str__(self) -> str:
        return str(self._value) + (f' {self._unit}' if self._unit is not None else '')

    def as_int(self) -> int:
        """Returns the numeric data as a Python int-object """
        return int(self._value)

    def as_float(self) -> float:
        """Returns the numeric data as a Python float-object"""
        return float(self._value)

    @property
    def unit(self) -> str:
        """Returns the unit as a Python str-object"""
        return self._unit

    def compose(self) -> str:
        """Composes the object into a SCPI string to be used as a parameter"""
        if type(self._value) == int:
            # Compose into NR1 representation
            return f'{self._value:d}{(" " + self._unit) if self._unit is not None else ""}'
        elif type(self._value) == float:
            # Compose into NR2/3 representation
            return f'{self._value:e}{(" " + self._unit) if self._unit is not None else ""}'
        else:
            raise TypeError

    @classmethod
    def parse(cls, transport: ScpiTransports):
        """Parses stream data from the device and creates a `ScpiNumber` object"""
        data = transport.readline()
        substrs = data.split(' ')
        try:
            # Try as NR1 representation first
            value = int(substrs[0])
        except ValueError:
            try:
                # Otherwise NR2 or NR3 representation
                value = float(substrs[0])
            except ValueError:
                raise TypeError

        # Unit available?
        if len(substrs) > 1:
            unit = substrs[1]
        else:
            unit = None

        return ScpiNumber(value, unit)

class ScpiNumberArray(ScpiTypeBase):
    """
    Class representing an array of IEEE488.2 flexible Decimal/Nondecimal numeric NRf program data (7.7.2/7.7.4) and
    NR1/NR2/NR3 response data (8.7.2/8.7.3/8.7.4)
    """

    def __init__(self, array: Union[List[int], List[float]]) -> None:
        """Initializes the object from a list of either an int (NR1) or float (NR2/NR3) values"""
        super().__init__()
        self._array = array

    def __str__(self) -> str:
        return str(self._array)

    def as_int_list(self) -> List[int]:
        """Returns the numeric data as a Python list of ints"""
        return [int(x) for x in self._array]

    def as_float_list(self) -> List[float]:
        """Returns the numeric data as a Python list of floats"""
        return [float(x) for x in self._array]

    def compose(self) -> str:
        """Composes the object into a SCPI string to be used as a parameter"""
        if type(self._array[0]) == int:
            # Compose into NR1 representation
            return ','.join([f'{x:d}' for x in self._array])
        elif type(self._array[0]) == float:
            # Compose into NR2/3 representation
            return ','.join([f'{x:e}' for x in self._array])
        else:
            raise TypeError

    @classmethod
    def parse(cls, transport: ScpiTransports):
        """Parses stream data from the device and creates a `ScpiNumber` object"""
        data = transport.readline()
        substrs = data.split(',')

        try:
            # Try as NR1 representation first
            array = [int(substr) for substr in substrs]
        except ValueError:
            try:
                array = [float(substr) for substr in substrs]
            except ValueError:
                raise TypeError

        return ScpiNumberArray(array)

class ScpiString(ScpiTypeBase):
    """"
    Class representing IEEE488.2 String program data (7.7.5) and response data (8.7.8)

        This element allows any character in the ASCII 7-bit code to be transmitted as a message.
        This data field is particularly useful where text is to be displayed.
    """

    def __init__(self, data: str) -> None:
        """Initializes the object from a str type"""
        super().__init__()
        self._data = data

    def __str__(self) -> str:
        # Shorten string for str() display
        s = self._data.replace('\r', '').replace('\n', ' ')
        s = s[:40] + (s[40:] and '...')
        return s

    def __bytes__(self) -> bytes:
        return self.as_bytes()

    def as_string(self) -> str:
        """Returns the char data as a Python str-object"""
        return self._data

    def as_bytes(self) -> bytes:
        """Returns the char data as a Python bytes-object"""
        return self._data.encode('ascii')

    def compose(self) -> str:
        """Composes the object into a SCPI string to be used as a parameter"""
        raise NotImplementedError

    @classmethod
    def parse(cls, transport: ScpiTransports):
        """Parses stream data from the device and creates a `ScpiString` object"""
        quotes = 0
        string = ""
        while 1:
            chunk = transport.readline()
            # TODO: double quotes

            quotes += chunk.count('"')
            string += chunk + '\r\n'

            if (quotes % 2 == 0) and (string != ''):
                break

        string = string.strip('\r\n\t"')
        return ScpiString(string)


class ScpiArbBlock(ScpiTypeBase):
    """
    Class representing IEEE488.2 Arbitrary block program data (7.7.6) and
    definite length arbitrary block response (8.7.9)

        This element allows any 8 bit bytes to be transmitted in a message.
        This element is particularly helpful for sending large quantities of data.
    """
    def __init__(self, data: bytes):
        super().__init__()
        self._data = data

    def __str__(self) -> str:
        return f'<block with {len(self._data)} bytes of binary data>'

    def __bytes__(self) -> bytes:
        return self.as_bytes()

    def as_bytes(self) -> bytes:
        return self._data

    def compose(self) -> str:
        length = f'{len(self._data)}'
        head = f'{len(length)}'
        return '#' + head + length + self._data.decode('iso-8859-15')

    @classmethod
    def parse(cls, transport: ScpiTransports):
        """Parses stream data from the device and creates a `ScpiArbBlock` object"""
        head = transport.read(2)

        if head[0:1] != b'#':
            raise ValueError("Could not find hash sign (#) indicating the start of the block.")

        # read header size
        num = int(head[1:2])

        if num == 0:
            raise NotImplementedError("Indefinite length arbitrary block response not implemented")

        # read header
        length = int(transport.read(num))
        data = transport.read(length)

        # Swallow \r\n
        transport.readline()

        return ScpiArbBlock(data)


class ScpiArbStream(ScpiTypeBase, io.RawIOBase):
    """
    Class representing IEEE488.2 Arbitrary block program data (7.7.6) and
    definite length arbitrary block response (8.7.9)

        This element allows any 8 bit bytes to be transmitted in a message.
        This element is particularly helpful for sending large quantities of data.

    Note that this class is derived from io.RawIOBase and can be used for stream processing
    """

    def __init__(self, transport: ScpiTransports, length: int) -> None:
        """Initialize object from a `ScpiTransportBase` object and length integer"""
        super().__init__()
        self._transport = transport
        self._length = length
        self._remaining = length

    def __str__(self) -> str:
        return f'<stream with {self._length} bytes of binary data>'

    def fileno(self) -> int:
        return self._transport.fileno()

    def close(self) -> None:
        pass

    def closed(self) -> bool:
        return False

    def isatty(self) -> bool:
        return self._transport.isatty()

    def readable(self) -> bool:
        return self._transport.readable()

    def readline(self, __size: Optional[int] = -1) -> bytes:
        raise NotImplementedError()

    def readlines(self, __hint: int = -1) -> List[bytes]:
        raise NotImplementedError()

    def seekable(self) -> bool:
        return self._transport.seekable()

    def writable(self) -> bool:
        return False

    def writelines(self, lines: Iterable):
        raise NotImplementedError()

    def read(self, __size: int = -1) -> Optional[bytes]:
        data = self._transport.read(__size)
        self._remaining -= len(data)

        if self._remaining == 0:
            # eat newline
            self._transport.readline()

        return data

    def readall(self) -> bytes:
        return self.read(self._remaining)

    def compose(self) -> str:
        raise NotImplementedError()

    @classmethod
    def parse(cls, transport: ScpiTransports):
        """Parses stream data from the device and creates a `ScpiArbStream` object"""
        head = transport.read(2)

        if head[0:1] != b'#':
            raise ValueError("Could not find hash sign (#) indicating the start of the block.")

        # read header size
        num = int(head[1:2])

        if num == 0:
            raise NotImplementedError("Indefinite length arbitrary block response not implemented")

        # read header
        length = int(transport.read(num))

        return ScpiArbStream(transport, length)


class ScpiBool(ScpiTypeBase):
    """
    Class representing SCPI-99 boolean (Vol. 1, 7.3)
    """

    def __init__(self, onoff: bool) -> None:
        """Initializes the object from a Python bool type"""
        super().__init__()
        self._onoff = onoff

    def __str__(self) -> str:
        return str(self._onoff)

    def __bool__(self) -> bool:
        return self.as_bool()

    def as_bool(self) -> bool:
        """Returns the boolean value as a Python bool type"""
        if self._onoff:
            return True
        else:
            return False

    def compose(self) -> str:
        """Composes the object into a SCPI string to be used as a parameter"""
        if self._onoff:
            return "ON"
        else:
            return "OFF"

    @classmethod
    def parse(cls, transport: ScpiTransports):
        """Parses stream data from the device and creates a `ScpiBool` object"""
        data = transport.readline()
        if int(data) == 0:
            return ScpiBool(False)
        else:
            return ScpiBool(True)


class ScpiNumList(ScpiTypeBase):
    """
    Class representing a SCPI-99 numeric list (Vol. 1, 8.8.3) using the
    IEEE488.2 Expression program data (7.7.7) and Expression response data (8.7.12) format.

        A numeric list is an expression format for compactly expressing
        numbers and ranges of numbers in a single parameter.
    """

    def __init__(self, numlist: List[int]) -> None:
        self._numlist = numlist

    def __str__(self) -> str:
        return str(self._numlist)

    def as_list(self) -> List[int]:
        """Returns the object as a Python list-object"""
        return self._numlist

    def compose(self) -> str:
        """Composes the numeric list into a SCPI string to be used as a parameter"""
        return '(' + ','.join(map(str, self._numlist)) + ')'

    @classmethod
    def parse(cls, transport: ScpiTransports):
        """Parses stream data from the device and creates a `ScpiNumList` object"""
        data = transport.readline()
        substrs = data.strip('()').split(',')
        return ScpiNumList([int(e) for e in substrs])


class ScpiEvent(ScpiTypeBase):
    """
    Class representing a SCPI-99 error/event queue item (Vol. 2, 21.8)
    """

    def __init__(self, code: int, description: str, info: Optional[str] = None) -> None:
        self._code = code
        self._description = description
        self._info = info

    def __str__(self) -> str:
        return self.as_string()

    def as_string(self) -> str:
        """Return the event as Python str-object"""
        return f'{self._code:d}: {self._description}' + (f' ({self._info})' if self._info is not None else '')

    @property
    def code(self):
        return self._code

    @property
    def description(self):
        return self._description

    @property
    def info(self):
        return self._info

    def compose(self) -> str:
        raise NotImplementedError

    @classmethod
    def parse(cls, transport: ScpiTransports):
        data = transport.readline()
        substrs = data.split(',')
        event = substrs[1].strip('"').split(';')
        code = int(substrs[0])
        description = event[0]
        info = event[1] if len(event) > 1 else None
        return ScpiEvent(code, description, info)
