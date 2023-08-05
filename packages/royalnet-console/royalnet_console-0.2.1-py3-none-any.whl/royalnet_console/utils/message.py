# Module docstring
"""
An universal function to send messages to the console.
"""

# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
import logging
import royalnet.engineer as engi

# Internal imports
# from . import something

# Special global objects
log = logging.getLogger(__name__)


# Code
async def console_message(*,
                          mag: engi.Magazine,
                          text: str = None,
                          files: t.List[t.BinaryIO] = None) -> engi.Message:
    """
    Output a message to the console and return the resulting bullet.

    :param mag: The :class:`.engi.Magazine` to use when instantiating the bullet.
    :param text: The text of the message.
    :param files: A :class:`list` of files to attach to the message.
    :return: The sent :class:`.engi.Message`.
    """
    if files is None:
        files = []

    if len(files) > 0:
        raise engi.exc.NotSupportedError("Console does not allow sending files.")

    log.debug("Sending message...")
    print(text)

    log.debug("Creating bullet...")
    return mag.Message(_text=text)


# Objects exported by this module
__all__ = (
    "console_message",
)
