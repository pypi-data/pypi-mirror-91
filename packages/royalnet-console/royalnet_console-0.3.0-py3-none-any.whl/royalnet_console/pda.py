# Module docstring
"""
The PDA ("main" class) for the :mod:`royalnet_console` frontend.
"""

# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
import logging
import asyncio
import royalnet.engineer as engi
import click

# Internal imports
from . import magazine

# Special global objects
log = logging.getLogger(__name__)


# Code
class ConsolePDA:
    """
    A PDA which handles :mod:`royalnet` input and output using a terminal as source.
    """

    def __init__(self):
        log.debug(f"Creating new ConsolePDA...")

        log.debug(f"Creating new magazine...")
        self.mag = magazine.ConsoleMagazine()
        """
        The :class:`royalnet.engineer.magazine.Magazine` used by this PDA.
        """

        self.dispenser: t.Optional[engi.Dispenser] = None
        """
        The :class:`royalnet.engineer.dispenser.Dispenser` of this PDA.
        """

        self.conversations: t.List[engi.Conversation] = []
        """
        A :class:`list` of conversations to run before a new event is :meth:`.put` in a 
        :class:`~royalnet.engineer.dispenser.Dispenser`.
        """

    async def run(self) -> t.NoReturn:
        """
        Run the main loop of the :class:`.ConsolePDA`.
        """

        while True:
            message = click.prompt("", type=str, prompt_suffix=">>> ", show_default=False)
            log.debug(f"Received a new message: {message!r}")

            log.debug(f"Creating ConsoleMessage from: {message!r}")
            bullet = self.mag.Message(_text=message)

            log.debug(f"Putting bullet: {bullet!r}")
            await self.put_bullet(bullet=bullet)

    def register_conversation(self, conv: engi.Conversation) -> None:
        """
        Register a new conversation in the PDA.

        :param conv: The conversation to register.
        """
        log.info(f"Registering conversation: {conv!r}")
        self.conversations.append(conv)

    def unregister_conversation(self, conv: engi.Conversation) -> None:
        """
        Unregister a conversation from the PDA.

        :param conv: The conversation to unregister.
        """
        log.info(f"Unregistering conversation: {conv!r}")
        self.conversations.remove(conv)

    def register_partial(self, part: engi.PartialCommand, names: t.List[str]) -> engi.Command:
        """
        Register a new :class:`~royalnet.engineer.command.PartialCommand` in the PDA, converting it to a
        :class:`royalnet.engineer.Command` in the process.

        :param part: The :class:`~royalnet.engineer.command.PartialCommand` to register.
        :param names: The :attr:`~royalnet.engineer.command.Command.names` to register the command with.
        :return: The resulting :class:`~royalnet.engineer.command.Command`.
        """
        log.debug(f"Completing partial: {part!r}")
        if part.syntax:
            command = part.complete(pattern=r"^{name}\s+{syntax}$", names=names)
        else:
            command = part.complete(pattern=r"^{name}$", names=names)
        self.register_conversation(command)
        return command

    async def put_bullet(self, bullet: engi.Bullet) -> None:
        """
        Insert a new bullet into the dispenser.

        :param bullet: The bullet to put in the dispenser.
        """
        if not self.dispenser:
            log.debug(f"Dispenser not found, creating one...")
            self.dispenser = engi.Dispenser()

        log.debug("Getting running loop...")
        loop = asyncio.get_running_loop()

        for conversation in self.conversations:
            log.debug(f"Creating run task for: {conversation!r}")
            loop.create_task(self.dispenser.run(conversation), name=f"{repr(conversation)}")

        log.debug("Running a event loop cycle...")
        await asyncio.sleep(0)

        log.debug(f"Putting bullet {bullet!r} in dispenser {self.dispenser!r}...")
        await self.dispenser.put(bullet)

        log.debug("Awaiting another event loop cycle...")
        await asyncio.sleep(0)


# Objects exported by this module
__all__ = (
    "ConsolePDA",
)
