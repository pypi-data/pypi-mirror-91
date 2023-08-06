# Module docstring
"""
The :class:`royalnet.engineer.magazine.Magazine` for the :mod:`royalnet_discordpy` frontend.
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
class DiscordMagazine(engi.Magazine):
    _USER = bullets.DiscordUser
    _CHANNEL = bullets.DiscordChannel
    _MESSAGE = bullets.DiscordMessage


# Objects exported by this module
__all__ = (
    "",
)
