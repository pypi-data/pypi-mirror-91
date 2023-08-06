import asyncio

import async_timeout

from ...._errors import ProxyConnectionError, ProxyTimeoutError
from ...._proto_http_async import HttpProto
from ...._proto_socks4_async import Socks4Proto
from ...._proto_socks5_async import Socks5Proto

from ._stream import SocketStream

DEFAULT_TIMEOUT = 60


class BaseProxy:
    def __init__(self, proxy_host, proxy_port, proxy_ssl=None,
                 loop: asyncio.AbstractEventLoop = None):

        if loop is None:
            loop = asyncio.get_event_loop()

        self._loop = loop

        self._proxy_host = proxy_host
        self._proxy_port = proxy_port
        self._proxy_ssl = proxy_ssl

        self._dest_host = None
        self._dest_port = None
        self._timeout = None

        self._stream = SocketStream(loop=loop)

    async def connect(self, dest_host, dest_port, timeout=DEFAULT_TIMEOUT):
        self._dest_host = dest_host
        self._dest_port = dest_port
        self._timeout = timeout

        try:
            await self._connect()
        except asyncio.TimeoutError as e:
            raise ProxyTimeoutError(
                'Proxy connection timed out: %s'
                % self._timeout) from e

        return self._stream

    async def _connect(self):
        async with async_timeout.timeout(self._timeout):
            try:
                await self._stream.open_connection(
                    host=self._proxy_host,
                    port=self._proxy_port,
                )
                if self._proxy_ssl is not None:
                    await self._stream.start_tls(
                        hostname=self._proxy_host,
                        ssl_context=self._proxy_ssl
                    )
            except OSError as e:
                await self._stream.close()
                msg = ('Can not connect to proxy %s:%s [%s]' %
                       (self._proxy_host, self._proxy_port, e.strerror))
                raise ProxyConnectionError(e.errno, msg) from e
            except Exception:  # pragma: no cover
                await self._stream.close()
                raise

            try:
                await self.negotiate()
            except Exception:
                await self._stream.close()
                raise

    async def negotiate(self):
        raise NotImplementedError()  # pragma: no cover

    @property
    def proxy_host(self):
        return self._proxy_host

    @property
    def proxy_port(self):
        return self._proxy_port


class Socks5Proxy(BaseProxy):
    def __init__(self, proxy_host, proxy_port,
                 username=None, password=None, rdns=None,
                 proxy_ssl=None,
                 loop: asyncio.AbstractEventLoop = None):
        super().__init__(
            proxy_host=proxy_host,
            proxy_port=proxy_port,
            proxy_ssl=proxy_ssl,
            loop=loop
        )
        self._username = username
        self._password = password
        self._rdns = rdns

    async def negotiate(self):
        proto = Socks5Proto(
            stream=self._stream,  # noqa
            dest_host=self._dest_host,
            dest_port=self._dest_port,
            username=self._username,
            password=self._password,
            rdns=self._rdns
        )
        await proto.negotiate()


class Socks4Proxy(BaseProxy):
    def __init__(self, proxy_host, proxy_port,
                 user_id=None, rdns=None, proxy_ssl=None,
                 loop: asyncio.AbstractEventLoop = None):
        super().__init__(
            proxy_host=proxy_host,
            proxy_port=proxy_port,
            proxy_ssl=proxy_ssl,
            loop=loop
        )
        self._user_id = user_id
        self._rdns = rdns

    async def negotiate(self):
        proto = Socks4Proto(
            stream=self._stream,  # noqa
            dest_host=self._dest_host,
            dest_port=self._dest_port,
            user_id=self._user_id,
            rdns=self._rdns
        )
        await proto.negotiate()


class HttpProxy(BaseProxy):
    def __init__(self, proxy_host, proxy_port,
                 username=None, password=None, proxy_ssl=None,
                 loop: asyncio.AbstractEventLoop = None):
        super().__init__(
            proxy_host=proxy_host,
            proxy_port=proxy_port,
            proxy_ssl=proxy_ssl,
            loop=loop
        )
        self._username = username
        self._password = password

    async def negotiate(self):
        proto = HttpProto(
            stream=self._stream,  # noqa
            dest_host=self._dest_host,
            dest_port=self._dest_port,
            username=self._username,
            password=self._password
        )
        await proto.negotiate()
