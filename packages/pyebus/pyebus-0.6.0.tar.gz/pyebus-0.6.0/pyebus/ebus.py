"""Pythonic EBUS Representation."""
import asyncio
import collections
import logging

from .connection import CommandError, Connection, ConnectionTimeout
from .msg import filter_msg
from .msgdecoder import MsgDecoder, UnknownMsgError
from .msgdefdecoder import decode_msgdef
from .msgdefs import MsgDefs
from .util import repr_

_LOGGER = logging.getLogger(__name__)
_CMD_FINDMSGDEFS = "find -a -F type,circuit,name,fields"


class Ebus:

    """
    Pythonic EBUS Representation.

    This instance connects to an EBUSD instance and allows to read, write or monitor.
    """

    def __init__(self, host, port, timeout=10, scanwaitinterval=3, msgdefs=None):
        self.connection = Connection(host=host, port=port, autoconnect=True, timeout=timeout)
        self.scanwaitinterval = scanwaitinterval
        self._msgdefs = msgdefs
        self.msgdecoder = MsgDecoder(msgdefs or MsgDefs())
        _LOGGER.info(f"{self}")

    def __repr__(self):
        return repr_(
            self,
            args=(self.connection.host, self.connection.port),
            kwargs=(
                ("timeout", self.timeout, 10),
                ("scanwaitinterval", self.scanwaitinterval, 3),
                ("msgdefs", self._msgdefs, None),
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
        return Ebus(
            self.host, self.port, timeout=self.timeout, scanwaitinterval=self.scanwaitinterval, msgdefs=self.msgdefs
        )

    async def wait_scancompleted(self):
        """Wait until scan is completed."""
        cnts = []
        while True:
            cnt = sum([1 async for line in self._request(_CMD_FINDMSGDEFS)])
            cnts.append(cnt)
            if len(cnts) < 4 or cnts[-4] != cnts[-3] or cnts[-3] != cnts[-2] or cnts[-2] != cnts[-1]:
                await asyncio.sleep(self.scanwaitinterval)
            else:
                break

    async def load_msgdefs(self):
        """
        Load Message Definitions from EBUSD.

        Keyword Args:
            scanwait(bool): Wait for EBUSD scan to complete
        """
        _LOGGER.info("load_msgdefs()")
        self.msgdefs.clear()
        msgdefs = []
        async for line in self._request(_CMD_FINDMSGDEFS):
            if line:
                try:
                    msgdef = decode_msgdef(line)
                    if not msgdef.circuit.startswith("scan"):
                        msgdefs.append(msgdef)
                except ValueError as exc:
                    _LOGGER.warning(f"Cannot decode message definition ({exc})")
        for msgdef in sorted(msgdefs, key=lambda msgdef: (msgdef.circuit, msgdef.name)):
            self.msgdefs.add(msgdef)

    async def read(self, msgdef, defaultprio=None, setprio=False, ttl=None):
        """
        Read Message.

        Raises:
            ValueError: on decoder error
        """
        _LOGGER.info(f"read({msgdef!r}, defaultprio={defaultprio!r}, setprio={setprio!r}, ttl={ttl!r})")
        prio = msgdef.prio or defaultprio if setprio else None
        try:
            lines = tuple([line async for line in self._request("read", msgdef.name, c=msgdef.circuit, p=prio, m=ttl)])
        except CommandError as exc:
            _LOGGER.warning(f"{msgdef.ident}: {exc!r}")
        else:
            return self.msgdecoder.decode_value(msgdef, lines[0])

    async def write(self, msgdef, value, ttl=0):
        """Write Message."""
        _LOGGER.info(f"write({msgdef!r}, value={value!r}, ttl={ttl!r})")
        if not msgdef.write:
            raise ValueError(f"Message is not writeable '{msgdef}'")
        fullmsgdef = self.msgdefs.get(msgdef.circuit, msgdef.name)
        if fullmsgdef != msgdef:
            # Read
            if not msgdef.read:
                raise ValueError(f"Message is not read-modify-writable '{msgdef}'")
            readline = tuple([line async for line in self._request("read", msgdef.name, c=msgdef.circuit, m=ttl)])[0]
            values = readline.split(";")
            # Modify
            for fielddef in msgdef.fields:
                encvalue = fielddef.type_.encode(value)
                values[fielddef.idx] = encvalue
        else:
            values = [fielddef.type_.encode(value) for fielddef in msgdef.fields]
        # Write
        async for _ in self._request("write", msgdef.name, ";".join(values), c=msgdef.circuit, check=True):
            pass

    async def listen(self, msgdefs=None):
        """Listen to EBUSD, decode and yield."""
        _LOGGER.info(f"listen(msgdefs={msgdefs!r})")
        async for line in self._request("listen", infinite=True):
            if line == "listen started":
                continue
            msg = self._decode_line(line)
            if msg is not None and msgdefs is not None:
                msg = filter_msg(msg, msgdefs)
            if msg:
                yield msg

    async def observe(self, msgdefs=None, defaultprio=None, setprio=False, ttl=None):
        """
        Observe.

        Read all known messages.
        Use `find` to get the latest data, if me missed any updates in the
        meantime and start listening
        """
        _LOGGER.info(f"observe(msgdefs={msgdefs!r}, defaultprio={defaultprio!r}, setprio={setprio!r}, ttl={ttl!r})")
        msgdefs = msgdefs or self.msgdefs
        data = collections.defaultdict(lambda: None)

        # read all
        for msgdef in msgdefs:
            if msgdef.read:
                msg = await self.read(msgdef, defaultprio=defaultprio, setprio=setprio, ttl=ttl)
                if msg.valid:
                    msg = filter_msg(msg, msgdefs)
                if msg.valid:
                    data[msgdef] = msg
                yield msg
            elif msgdef.update:
                data[msgdef] = None

        # find new values (which got updated while we where reading)
        async for line in self._request("find -d"):
            msg = self._decode_line(line)
            if msg:
                msg = filter_msg(msg, msgdefs)
            if msg and msg != data[msg.msgdef]:
                yield msg
                data[msg.msgdef] = msg

        # listen
        async for msg in self.listen(msgdefs=msgdefs):
            yield msg

    async def get_state(self):
        """Return state string."""
        _LOGGER.info("get_state()")
        try:
            lines = tuple([line async for line in self._request("state")])
            state = lines[0].split(",")[0]
            if state == "signal acquired":
                return "ok"
            else:
                return state
        except ConnectionTimeout:
            return "no ebusd connection"

    async def is_online(self):
        """Return if we are online."""
        state = await self.get_state()
        return state == "ok"

    async def cmd(self, cmd, infinite=False, check=False):
        """Send `cmd` to EBUSD and Receive Response."""
        _LOGGER.info(f"cmd({cmd!r}, infinite={infinite!r}, check={check!r})")
        await self.connection.write(cmd)
        async for line in self.connection.readlines(infinite=infinite, check=check):
            yield line

    async def _request(self, cmd, *args, infinite=False, check=False, **kwargs):
        """Assemble request, send and readlines."""
        parts = [cmd]
        parts += [f"-{option} {value}" for option, value in kwargs.items() if value is not None]
        parts += [str(arg) for arg in args]
        await self.connection.write(" ".join(parts))
        async for line in self.connection.readlines(infinite=infinite, check=check):
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
