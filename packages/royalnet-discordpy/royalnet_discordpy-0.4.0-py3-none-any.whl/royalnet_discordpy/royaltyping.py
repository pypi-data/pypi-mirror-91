"""
Additional typing annotations for the :mod:`royalnet_discordpy` frontend.
"""

from __future__ import annotations
import royalnet.royaltyping as t

import discord

MsgChannel = t.Union[discord.TextChannel, discord.DMChannel, discord.GroupChannel]
"""
A channel where messages can be sent. Slightly different from :class:`discord.Messageable`, as it does not include 
users.
"""

__all__ = (
    "MsgChannel",
)
