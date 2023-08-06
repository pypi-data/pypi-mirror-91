"""EBUS Connection Handling."""
import asyncio
import logging

from .util import repr_

_LOGGER = logging.getLogger(__name__)


class Connection:
    """
    EBUS Connection.

    Keyword Args:
        host (str): Hostname or IP
        port (int): Port
        autoconnect (bool): Automatically connect and re-connect
    """

    def __init__(self, host="127.0.0.1", port=8888, autoconnect=False, timeout=None):
        self._host = host
        self._port = port
        self._autoconnect = autoconnect
        self._timeout = timeout
        self._reader, self._writer = None, None

    def __repr__(self):
        return repr_(
            self,
            kwargs=(
                ("host", self.host, "127.0.0.1"),
                ("port", self.port, 8888),
                ("autoconnect", self.autoconnect, False),
                ("timeout", self.timeout, None),
            ),
        )

    @property
    def host(self):
        """Host."""
        return self._host

    @property
    def port(self):
        """Port."""
        return self._port

    @property
    def autoconnect(self):
        """Automatically connect and re-connect."""
        return self._autoconnect

    @property
    def timeout(self):
        """Connection Timeout."""
        return self._timeout

    async def async_connect(self):
        """
        Establish connection (required before first communication).

        Raises:
            IOError: If connection cannot be established
        """
        _LOGGER.debug("connect()")
        self._reader, self._writer = await self._async_timedout(asyncio.open_connection(self._host, self._port))

    async def async_disconnect(self):
        """Disconnect if not already done."""
        _LOGGER.debug("disconnect()")
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except BrokenPipeError:  # pragma: no cover
                pass
            finally:
                self._reader, self._writer = None, None

    def is_connected(self):
        """
        Return `True` if connection is established.

        This does not check if the connection is still usable.
        """
        return self._writer is not None and not self._writer.is_closing()

    async def async_write(self, message):
        """
        Send `message`.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        _LOGGER.debug(f"write({message!r})")
        await self._async_ensure_connection()
        self._writer.write(f"{message}\n".encode())
        await self._async_timedout(self._writer.drain())

    async def async_readline(self):
        """
        Receive one line.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        await self._async_ensure_connection()
        line = await self._async_readline()
        await self._async_checkline(line)
        _LOGGER.debug(f"async_readline() = {line!r}")
        return line

    async def async_readlines(self, infinite=False, check=False):
        """
        Receive lines until an empty one.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        await self._async_ensure_connection()
        while True:
            line = await self._async_readline()
            if check:
                await self._async_checkline(line)
            _LOGGER.debug(f"readlines() = {line!r}")
            yield line
            if not line and not infinite:
                break

    async def _async_readline(self):
        line = await self._reader.readline()
        return line.decode("utf-8").rstrip()

    async def _async_ensure_connection(self):
        if not self._writer or self._writer.is_closing():
            if self._autoconnect:
                await self.async_connect()
            else:
                raise ConnectionError("Not connected")

    async def _async_timedout(self, task):
        if self._timeout:
            try:
                result = await asyncio.wait_for(task, timeout=self._timeout)
            except asyncio.TimeoutError as timeout:
                raise ConnectionTimeout(f"{self.host}:{self.port}") from timeout
        else:
            result = await task
        return result

    async def _async_checkline(self, line):
        if line.startswith("ERR: "):
            # consume everything until newline
            while await self._async_readline():
                pass
            raise CommandError(line.lstrip("ERR: "))


class CommandError(RuntimeError):

    """Command Error raised in case of EBUSD error."""


class ConnectionTimeout(RuntimeError):

    """Connection Timeout."""
