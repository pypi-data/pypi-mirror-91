# Module docstring
"""
The PDA ("main" class) for the :mod:`royalnet_discordpy` frontend.
"""

# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
import discord
import logging
import asyncio
import royalnet.engineer as engi

# Internal imports
from . import magazine

# Special global objects
log = logging.getLogger(__name__)


# Code
class DiscordPDA(discord.AutoShardedClient):
    def __init__(self, *args, **kwargs):
        log.debug(f"Creating new DiscordPDA...")

        log.debug(f"Creating new magazine...")
        self.mag = magazine.DiscordMagazine()
        """
        The :class:`royalnet.engineer.magazine.Magazine` used by this PDA.
        """

        log.debug(f"Subscribing to guild_messages and dm_messages by setting intents...")
        intents = discord.Intents(guilds=True, members=True, guild_messages=True, dm_messages=True)

        log.debug(f"Initializing AutoShardedClient...")
        super().__init__(*args, intents=intents, **kwargs)
        self.dispensers: t.Dict[int, engi.Dispenser] = {}
        """
        A :class:`dict` which maps :class:`bullets.DiscordChannel`s to :class:`royalnet.engineer.dispenser.Dispenser`s.
        """

        self.conversations: t.List[engi.Conversation] = []
        """
        A :class:`list` of conversations to run before a new event is :meth:`.put` in a 
        :class:`~royalnet.engineer.dispenser.Dispenser`.
        """

    @staticmethod
    async def on_shard_connect(shard_id):
        log.info(f"Shard #{shard_id} connected to Discord")

    @staticmethod
    async def on_shard_disconnect(shard_id):
        log.warning(f"Shard #{shard_id} disconnected from Discord")

    @staticmethod
    async def on_shard_ready(shard_id):
        log.info(f"Shard #{shard_id} is ready")

    @staticmethod
    async def on_shard_resumed(shard_id):
        log.info(f"Shard #{shard_id} resumed connection")

    async def on_error(self, event_method, *args, **kwargs):
        """
        .. todo:: Maybe the behaviour of re-raising errors should be changed...
        """
        raise

    async def on_message(self, message: discord.Message):
        log.debug(f"Received a new message: {message!r}")

        if message.type != discord.MessageType.default:
            log.debug(f"Ignoring message because type is: {message.type!r}")
            return

        author: t.Union[discord.User, discord.Member] = message.author
        if self.user.id == author.id:
            log.debug(f"Ignoring message from myself")
            return

        log.debug(f"Creating DiscordMessage from: {message!r}")
        bullet = self.mag.Message(_msg=message)

        log.debug(f"Getting the channel of: {bullet!r}")
        channel = await bullet.channel()

        log.debug(f"Putting bullet {bullet!r} in channel {channel!r}")
        await self.put_bullet(channel=channel, bullet=bullet)

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
        Register a new :class:`PartialCommand` in the PDA, converting it to a :class:`Command` in the process.

        :param part: The :class:`PartialCommand` to register.
        :param names: The :attr:`~royalnet.engineer.Command.names` to register the command as.
        :return: The resulting :class:`Command`.
        """
        log.debug(f"Completing partial: {part!r}")
        if part.syntax:
            command = part.complete(pattern=r"^!{name}\s+{syntax}$", names=names)
        else:
            command = part.complete(pattern=r"^!{name}$", names=names)
        self.register_conversation(command)
        return command

    async def put_bullet(self, channel: engi.Channel, bullet: engi.Bullet) -> None:
        """
        Insert a new bullet into the dispenser corresponding to the specified channel.

        :param channel: The channel associated to the dispenser the bullet should be put in.
        :param bullet: The bullet to put in the dispenser.
        """
        log.debug(f"Finding dispenser for channel: {channel!r}")
        dispenser = self.dispensers.get(hash(channel))
        if not dispenser:
            log.debug(f"Dispenser not found, creating one...")
            dispenser = engi.Dispenser()
            self.dispensers[hash(channel)] = dispenser

        log.debug("Getting running loop...")
        loop = asyncio.get_running_loop()

        for conversation in self.conversations:
            log.debug(f"Creating run task for: {conversation!r}")
            loop.create_task(dispenser.run(conversation), name=f"{repr(conversation)}")

        log.debug("Running a event loop cycle...")
        await asyncio.sleep(0)

        log.debug(f"Putting bullet {bullet!r} in dispenser {dispenser!r}...")
        await dispenser.put(bullet)

        log.debug("Awaiting another event loop cycle...")
        await asyncio.sleep(0)


# Objects exported by this module
__all__ = (
    "DiscordPDA",
)
