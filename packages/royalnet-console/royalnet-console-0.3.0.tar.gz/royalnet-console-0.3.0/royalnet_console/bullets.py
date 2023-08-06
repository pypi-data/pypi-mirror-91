# Module docstring
"""
:class:`royalnet.engineer.bullet.Bullet`\\ s for the :mod:`royalnet_console` frontend.
"""

# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
import logging
import datetime
import os
import getpass
import psutil
import royalnet.engineer as engi

# Internal imports
from .utils.message import console_message

# Special global objects
log = logging.getLogger(__name__)


# Code
class ConsoleUser(engi.User):
    def __init__(self, mag: engi.Magazine):
        super().__init__(mag)

    def __hash__(self) -> int:
        return os.getuid()

    async def name(self) -> str:
        return getpass.getuser()

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> engi.Message:
        return await console_message(mag=self.mag, text=text, files=files)


class ConsoleChannel(engi.Channel):
    def __init__(self, mag: engi.Magazine):
        super().__init__(mag)

    def __hash__(self) -> int:
        return os.getpid()

    async def name(self) -> str:
        return psutil.Process(os.getpid()).name()

    async def users(self) -> t.List[engi.User]:
        return [self.mag.User()]

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> engi.Message:
        return await console_message(mag=self.mag, text=text, files=files)


class ConsoleMessage(engi.Message):
    _instance_count: int = 0

    def __init__(self, mag: engi.Magazine, _text: str, _timestamp: datetime.datetime = None):
        super().__init__(mag)
        self._text: str = _text
        self._timestamp: datetime.datetime = _timestamp or datetime.datetime.now()
        self._instance_number: int = self._instance_count
        self._instance_count += 1

    def __hash__(self) -> int:
        return self._instance_number

    async def text(self) -> str:
        return self._text

    async def timestamp(self) -> datetime.datetime:
        return self._timestamp

    async def channel(self) -> engi.Channel:
        return self.mag.Channel()

    async def send_reply(self, *,
                         text: str = None,
                         files: t.List[t.BinaryIO] = None) -> engi.Message:
        return await console_message(mag=self.mag, text=text, files=files)


# Objects exported by this module
__all__ = (
    "ConsoleUser",
    "ConsoleChannel",
    "ConsoleMessage",
)
