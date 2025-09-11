#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import load_config
import asyncio
import logging
import sys


class Client(object):
    """Client to send commands over socket to the daemon"""

    def __init__(self, debug=False):
        """Initialize ."""
        self.logger = logging.getLogger(__name__)
        log_lvl = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(stream=sys.stdout, level=log_lvl)
        self._config = load_config()

    async def _send_to_daemon(self, cmd):
        try:
            reader, writer = await asyncio.open_unix_connection(self._config.get('socket_path'))
        except FileNotFoundError:
            self.logger.error('daemon is not running')
            sys.exit(1)

        logging.debug(f'sending command [{cmd}]')
        writer.write(f'{cmd}\n'.encode())
        await writer.drain()

        logging.debug('closing the connection')
        writer.close()
        await writer.wait_closed()

    def send_cmd(self, cmd):
        asyncio.run(self._send_to_daemon(cmd))
