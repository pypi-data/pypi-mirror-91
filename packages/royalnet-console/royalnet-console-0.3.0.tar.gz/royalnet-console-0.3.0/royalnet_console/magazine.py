# Module docstring
"""
The :class:`royalnet.engineer.magazine.Magazine` for the :mod:`royalnet_console` frontend.
"""

# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
import logging
import royalnet.engineer as engi

# Internal imports
from . import bullets

# Special global objects
log = logging.getLogger(__name__)


# Code
class ConsoleMagazine(engi.Magazine):
    _USER = bullets.ConsoleUser
    _CHANNEL = bullets.ConsoleChannel
    _MESSAGE = bullets.ConsoleMessage


# Objects exported by this module
__all__ = (
    "ConsoleMagazine",
)
