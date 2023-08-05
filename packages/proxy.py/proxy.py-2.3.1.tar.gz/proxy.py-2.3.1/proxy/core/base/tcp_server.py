# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.
"""
from abc import abstractmethod
import socket
import selectors

from typing import Dict, Any, Optional

from proxy.core.acceptor import Work
from proxy.common.types import Readables, Writables


class BaseTcpServerHandler(Work):
    """BaseTcpServerHandler implements Work interface.

    An instance of BaseTcpServerHandler is created for each client
    connection.  BaseServerHandler lifecycle is controlled by
    Threadless core using asyncio.

    BaseServerHandler ensures that pending buffers are flushed
    before client connection is closed.

    Implementations must provide:
    a) handle_data(data: memoryview)
    c) (optionally) intialize, is_inactive and shutdown methods
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.must_flush_before_shutdown = False
        print('Connection accepted from {0}'.format(self.client.addr))

    @abstractmethod
    def handle_data(self, data: memoryview) -> Optional[bool]:
        """Optionally return True to close client connection."""
        pass    # pragma: no cover

    def get_events(self) -> Dict[socket.socket, int]:
        events = {}
        # We always want to read from client
        # Register for EVENT_READ events
        if self.must_flush_before_shutdown is False:
            events[self.client.connection] = selectors.EVENT_READ
        # If there is pending buffer for client
        # also register for EVENT_WRITE events
        if self.client.has_buffer():
            if self.client.connection in events:
                events[self.client.connection] |= selectors.EVENT_WRITE
            else:
                events[self.client.connection] = selectors.EVENT_WRITE
        return events

    def handle_events(
            self,
            readables: Readables,
            writables: Writables) -> bool:
        """Return True to shutdown work."""
        do_shutdown = False
        if self.client.connection in readables:
            try:
                data = self.client.recv()
                if data is None:
                    # Client closed connection, signal shutdown
                    print(
                        'Connection closed by client {0}'.format(
                            self.client.addr))
                    do_shutdown = True
                else:
                    r = self.handle_data(data)
                    if isinstance(r, bool) and r is True:
                        print(
                            'Implementation signaled shutdown for client {0}'.format(
                                self.client.addr))
                        if self.client.has_buffer():
                            print(
                                'Client {0} has pending buffer, will be flushed before shutting down'.format(
                                    self.client.addr))
                            self.must_flush_before_shutdown = True
                        else:
                            do_shutdown = True
            except ConnectionResetError:
                print(
                    'Connection reset by client {0}'.format(
                        self.client.addr))
                do_shutdown = True

        if self.client.connection in writables:
            print('Flushing buffer to client {0}'.format(self.client.addr))
            self.client.flush()
            if self.must_flush_before_shutdown is True:
                do_shutdown = True
            self.must_flush_before_shutdown = False

        if do_shutdown:
            print(
                'Shutting down client {0} connection'.format(
                    self.client.addr))
        return do_shutdown
