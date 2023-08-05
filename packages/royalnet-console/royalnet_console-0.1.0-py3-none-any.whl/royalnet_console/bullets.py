"""
.. todo:: Document :mod:`royalnet_console.bullets`.
"""

from __future__ import annotations
import royalnet.royaltyping as t

from royalnet.engineer import bullet, magazine, exc
import logging
import datetime
import os
import getpass
import psutil

log = logging.getLogger(__name__)


async def send_message(*,
                       mag: magazine.Magazine,
                       text: str = None,
                       files: t.List[t.BinaryIO] = None) -> bullet.Message:
    if len(files) > 0:
        raise exc.NotSupportedError("Console does not allow sending files.")

    log.debug("Sending message...")
    print(text)

    log.debug("Creating bullet...")
    return mag.Message(_text=text)


class ConsoleUser(bullet.User):
    def __init__(self, mag: "magazine.Magazine"):
        super().__init__(mag)

    def __hash__(self) -> int:
        return os.getuid()

    async def name(self) -> str:
        return getpass.getuser()

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> bullet.Message:
        return await send_message(mag=self.mag, text=text, files=files)


class ConsoleChannel(bullet.Channel):
    def __init__(self, mag: "magazine.Magazine"):
        super().__init__(mag)

    def __hash__(self) -> int:
        return os.getpid()

    async def name(self) -> str:
        return psutil.Process(os.getpid()).name()

    async def users(self) -> t.List[bullet.User]:
        return [self.mag.User()]

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> bullet.Message:
        return await send_message(mag=self.mag, text=text, files=files)


class ConsoleMessage(bullet.Message):
    _instance_count: int = 0

    def __init__(self, mag: "magazine.Magazine", _text: str, _timestamp: datetime.datetime = None):
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

    async def channel(self) -> bullet.Channel:
        return self.mag.Channel()

    async def send_reply(self, *,
                         text: str = None,
                         files: t.List[t.BinaryIO] = None) -> bullet.Message:
        return await send_message(mag=self.mag, text=text, files=files)


class ConsoleMagazine(magazine.Magazine):
    _USER = ConsoleUser
    _CHANNEL = ConsoleChannel
    _MESSAGE = ConsoleMessage


__all__ = (
    "ConsoleUser",
    "ConsoleChannel",
    "ConsoleMessage",
    "ConsoleMagazine",
)
