"""Pythonic EBUS Representation."""
import asyncio
import collections
import logging

from .connection import CommandError, Connection
from .const import AUTO, OK
from .msg import BrokenMsg, filter_msg
from .msgdecoder import MsgDecoder, UnknownMsgError
from .msgdefdecoder import decode_msgdef
from .msgdefs import MsgDefs
from .util import get_autoprio, repr_

_LOGGER = logging.getLogger(__name__)
_CMD_FINDMSGDEFS = "find -a -F type,circuit,name,fields"


class Ebus:

    """
    Pythonic EBUS Representation.

    This instance connects to an EBUSD instance and allows to read, write or monitor.
    """

    def __init__(self, host, port, timeout=10, scaninterval=10, scans=3, msgdefs=None):
        self.connection = Connection(host=host, port=port, autoconnect=True, timeout=timeout)
        self.scaninterval = scaninterval
        self.scans = scans
        self.msgdefcodes = []
        self.msgdecoder = MsgDecoder(msgdefs or MsgDefs())
        _LOGGER.info(f"{self}")

    def __repr__(self):
        return repr_(
            self,
            args=(self.connection.host, self.connection.port),
            kwargs=(
                ("timeout", self.timeout, 10),
                ("scaninterval", self.scaninterval, 10),
                ("scans", self.scans, 3),
            ),
        )

    @property
    def host(self):
        """Host Name or IP."""
        return self.connection.host

    @property
    def port(self):
        """Port."""
        return self.connection.port

    @property
    def timeout(self):
        """Timeout."""
        return self.connection.timeout

    @property
    def msgdefs(self):
        """Message Defintions."""
        return self.msgdecoder.msgdefs

    @msgdefs.setter
    def msgdefs(self, msgdefs):
        self.msgdecoder.msgdefs = msgdefs

    def __copy__(self):
        return Ebus(self.host, self.port, timeout=self.timeout, scaninterval=self.scaninterval, msgdefs=self.msgdefs)

    async def async_wait_scancompleted(self):
        """Wait until scan is completed."""
        cnts = []
        while True:
            cnt = sum([1 async for line in self._async_request(_CMD_FINDMSGDEFS)])
            cnts.append(cnt)
            if len(cnts) < self.scans or not all(cnt == cnts[-1] for cnt in cnts[-self.scans : -1]):
                await asyncio.sleep(self.scaninterval)
            else:
                break

    async def async_load_msgdefs(self):
        """
        Load Message Definitions from EBUSD.

        Alias for `load_msgdefcodes` and `decode_msgdefcodes`.
        """
        await self.async_load_msgdefcodes()
        self.decode_msgdefcodes()

    async def async_load_msgdefcodes(self):
        """Load EBUS Message Definition Codes."""
        _LOGGER.info("load_msgdefcodes()")
        self.msgdefcodes = msgdefcodes = []
        async for line in self._async_request(_CMD_FINDMSGDEFS):
            line = line.strip()
            if line:
                try:
                    msgdef = decode_msgdef(line)
                except ValueError as exc:
                    _LOGGER.warning(f"Cannot decode message definition '{line}' ({exc})")
                if not msgdef.circuit.startswith("scan"):
                    msgdefcodes.append(line)

    def decode_msgdefcodes(self):
        """Decode `msgdefcodes` and use as `msgdefs`."""
        _LOGGER.info("decode_msgdefcodes()")
        # Decode
        msgdefs = []
        for msgdefcode in self.msgdefcodes:
            try:
                msgdefs.append(decode_msgdef(msgdefcode))
            except ValueError as exc:
                _LOGGER.warning(f"Cannot decode message definition '{msgdefcode}' ({exc})")
        # Sort
        self.msgdefs.clear()
        for msgdef in sorted(msgdefs, key=lambda msgdef: (msgdef.circuit, msgdef.name)):
            self.msgdefs.add(msgdef)

    async def async_read(self, msgdef, defaultprio=None, ttl=None):
        """
        Read Message.

        Raises:
            ValueError: on decoder error
        """
        _LOGGER.info(f"read({msgdef!r}, defaultprio={defaultprio!r}, ttl={ttl!r})")
        setprio = msgdef.setprio or defaultprio
        if setprio == AUTO:
            setprio = get_autoprio(msgdef)
        try:
            lines = tuple(
                [line async for line in self._async_request("read", msgdef.name, c=msgdef.circuit, p=setprio, m=ttl)]
            )
        except CommandError as exc:
            return BrokenMsg(msgdef, str(exc))
        else:
            return self.msgdecoder.decode_value(msgdef, lines[0])

    async def async_write(self, msgdef, value, ttl=0):
        """Write Message."""
        _LOGGER.info(f"write({msgdef!r}, value={value!r}, ttl={ttl!r})")
        if not msgdef.write:
            raise ValueError(f"Message is not writeable '{msgdef}'")
        fullmsgdef = self.msgdefs.get(msgdef.circuit, msgdef.name)
        if fullmsgdef != msgdef:
            # Read
            if not msgdef.read:
                raise ValueError(f"Message is not read-modify-writable '{msgdef}'")
            readline = tuple(
                [line async for line in self._async_request("read", msgdef.name, c=msgdef.circuit, m=ttl)]
            )[0]
            values = readline.split(";")
            # Modify
            for fielddef in msgdef.fields:
                encvalue = fielddef.type_.encode(value)
                values[fielddef.idx] = encvalue
        else:
            values = [str(fielddef.type_.encode(value)) for fielddef in msgdef.fields]
        # Write
        async for _ in self._async_request("write", msgdef.name, ";".join(values), c=msgdef.circuit):
            pass

    async def async_listen(self, msgdefs=None):
        """Listen to EBUSD, decode and yield."""
        _LOGGER.info(f"listen(msgdefs={msgdefs!r})")
        async for line in self._async_request("listen", infinite=True):
            if line == "listen started":
                continue
            msg = self._decode_line(line)
            msg = filter_msg(msg, msgdefs)
            if msg:
                yield msg

    async def async_observe(self, msgdefs=None, defaultprio=None, ttl=None):
        """
        Observe.

        Read all known messages.
        Use `find` to get the latest data, if me missed any updates in the
        meantime and start listening
        """
        _LOGGER.info(f"observe(msgdefs={msgdefs!r}, defaultprio={defaultprio!r}, ttl={ttl!r})")
        msgdefs = msgdefs or self.msgdefs
        data = collections.defaultdict(lambda: None)

        # read all
        for msgdef in msgdefs:
            if msgdef.read:
                msg = await self.async_read(msgdef, defaultprio=defaultprio, ttl=ttl)
                msg = filter_msg(msg, msgdefs)
                if msg:
                    if msg.valid:
                        data[msgdef.ident] = msg
                    yield msg
            elif msgdef.update:
                data[msgdef.ident] = None

        # find new values (which got updated while we where reading)
        async for line in self._async_request("find -d"):
            msg = self._decode_line(line)
            msg = filter_msg(msg, msgdefs)
            if msg and msg != data[msg.msgdef.ident]:
                yield msg
                data[msg.msgdef.ident] = msg

        # listen
        async for msg in self.async_listen(msgdefs=msgdefs):
            yield msg

    async def async_get_state(self):
        """Return state string."""
        _LOGGER.info("get_state()")
        try:
            lines = tuple([line async for line in self._async_request("state")])
            state = lines[0].split(",")[0]
            if state == "signal acquired":
                return OK
            else:
                return state
        except Exception:  # pylint: disable=W0703
            return "no ebusd connection"

    async def async_is_online(self):
        """Return if we are online."""
        state = await self.async_get_state()
        return state == OK

    async def async_get_info(self):
        """Return info dict."""
        _LOGGER.info("get_info()")
        info = {}
        async for line in self._async_request("info"):
            if line:
                name, value = line.split(":", 1)
                info[name.strip()] = value.strip()
        return info

    async def async_cmd(self, cmd, infinite=False, check=False):
        """Send `cmd` to EBUSD and Receive Response."""
        _LOGGER.info(f"cmd({cmd!r}, infinite={infinite!r})")
        await self.connection.async_write(cmd)
        async for line in self.connection.async_readlines(infinite=infinite, check=check):
            yield line

    async def _async_request(self, cmd, *args, infinite=False, **kwargs):
        """Assemble request, send and readlines."""
        parts = [cmd]
        parts += [f"-{option} {value}" for option, value in kwargs.items() if value is not None]
        parts += [str(arg) for arg in args]
        await self.connection.async_write(" ".join(parts))
        async for line in self.connection.async_readlines(infinite=infinite):
            yield line

    def _decode_line(self, line):
        if line:
            try:
                return self.msgdecoder.decode_line(line)
            except UnknownMsgError:
                return None
            except ValueError as exc:
                _LOGGER.warning(f"Cannot decode message in {line!r}: {exc}")
        else:
            return None
