# Module docstring
"""
:class:`royalnet.engineer.bullet.Bullet`\\ s for the :mod:`royalnet_discordpy` frontend.
"""

# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
from royalnet.engineer import bullet, magazine, exc
import logging
import discord
import datetime

# Internal imports
from .royaltyping import MsgChannel

# Special global objects
log = logging.getLogger(__name__)


# Code
class DiscordUser(bullet.User):
    def __init__(self, mag: "magazine.Magazine", _user: discord.User):
        super().__init__(mag)
        self._user: discord.User = _user

    def __hash__(self) -> int:
        return self._user.id

    async def name(self) -> str:
        return f"{self._user.name}#{self._user.discriminator}"

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> bullet.Message:
        if len(files) > 10:
            log.warning(f"Attempted to send more than 10 files at a time: {files!r}")
            raise exc.NotSupportedError("Discord does not allow sending more than 10 files at a time.")

        log.debug(f"Converting files to discord.File: {files!r}")
        files = [discord.File(file) for file in files] if files is not None else []

        log.debug("Sending message...")
        _msg = await self._user.send(content=text, files=files)

        log.debug(f"Returning bullet: {_msg!r}")
        return self.mag.Message(_msg=_msg)


class DiscordChannel(bullet.Channel):
    def __init__(self, mag: "magazine.Magazine", _ch: MsgChannel):
        super().__init__(mag)
        self._ch: MsgChannel = _ch

    def __hash__(self) -> int:
        return self._ch.id

    async def name(self) -> str:
        return self._ch.name

    async def topic(self) -> str:
        return self._ch.topic

    async def users(self) -> t.List[bullet.User]:
        return [self.mag.User(_user=member) for member in self._ch.members]

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> bullet.Message:
        if len(files) > 10:
            log.warning(f"Attempted to send more than 10 files at a time: {files!r}")
            raise exc.NotSupportedError("Discord does not allow sending more than 10 files at a time.")

        log.debug(f"Converting files to discord.File: {files!r}")
        files = [discord.File(file) for file in files] if files is not None else []

        log.debug("Sending message...")
        _msg = await self._ch.send(content=text, files=files)

        log.debug(f"Returning bullet: {_msg!r}")
        return self.mag.Message(_msg=_msg)


class DiscordMessage(bullet.Message):
    def __init__(self, mag: "magazine.Magazine", _msg: discord.Message):
        super().__init__(mag)
        self._msg: discord.Message = _msg

    def __hash__(self) -> int:
        return self._msg.id

    async def text(self) -> str:
        return self._msg.content

    async def timestamp(self) -> datetime.datetime:
        return self._msg.created_at

    async def reply_to(self) -> bullet.Message:
        return self.mag.Message(_msg=self._msg.reference)

    async def channel(self) -> bullet.Channel:
        return self.mag.Channel(_ch=self._msg.channel)

    async def send_reply(self, *,
                         text: str = None,
                         files: t.List[t.BinaryIO] = None) -> bullet.Message:
        if len(files) > 10:
            log.warning(f"Attempted to send more than 10 files at a time: {files!r}")
            raise exc.NotSupportedError("Discord does not allow sending more than 10 files at a time.")

        log.debug(f"Converting files to discord.File: {files!r}")
        files = [discord.File(file) for file in files] if files is not None else []

        log.debug("Sending message...")
        _msg = await self._msg.channel.send(content=text, files=files)

        log.debug(f"Returning bullet: {_msg!r}")
        return self.mag.Message(_msg=_msg)


# Objects exported by this module
__all__ = (
    "DiscordUser",
    "DiscordChannel",
    "DiscordMessage",
)
