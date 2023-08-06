

# region [Imports]

# * Standard Library Imports -->

import asyncio
import gc
import logging
import os
import re
import sys
import json
import lzma
import time
import queue
import logging
import platform
import subprocess
from enum import Enum, Flag, auto
from time import sleep
from pprint import pprint, pformat
from typing import Union, Iterable
from datetime import tzinfo, datetime, timezone, timedelta
from functools import wraps, lru_cache, singledispatch, total_ordering, partial
from contextlib import contextmanager
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# * Third Party Imports -->

import discord
from discord.ext import commands, tasks


# * Gid Imports -->

import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.exceptions import MissingAttachmentError, NotAllowedChannelError, NotNecessaryRole, IsNotTextChannelError
from antipetros_discordbot.utility.misc import casefold_list, casefold_contains
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

# region [Constants]


# endregion[Constants]


def in_allowed_channels(allowed_channels: Iterable):
    def predicate(ctx):
        return ctx.channel.name in allowed_channels if not isinstance(ctx.channel, discord.DMChannel) else False
    return commands.check(predicate)


def log_invoker(logger, level: str = 'info'):
    def predicate(ctx):
        channel_name = ctx.channel.name if ctx.channel.type is discord.ChannelType.text else 'DM'
        getattr(logger, level)("command '%s' as '%s' -- invoked by: name: '%s', id: %s -- in channel: '%s' -- raw invoking message: '%s'",
                               ctx.command.name, ctx.invoked_with, ctx.author.name, ctx.author.id, channel_name, ctx.message.content)

        return True
    return commands.check(predicate)


def purge_check_from_user(user_id: int):

    def is_from_user(message):
        return message.author.id == user_id
    return is_from_user


def purge_check_contains(word: str, case_sensitive=False):
    def contains_in_content(message):
        content = message.content
        check_word = word
        if case_sensitive is False:
            content = message.content.casefold()
            check_word = word.casefold()
        return check_word in content.split()
    return contains_in_content


def purge_check_is_bot():
    def message_is_from_bot(message):
        return message.author.bot
    return message_is_from_bot


def purge_check_always_true():
    def always_true(message):
        return True
    return always_true


def purge_check_always_false():
    def always_false(message):
        return False
    return always_false


PURGE_CHECK_TABLE = {'is_bot': purge_check_is_bot,
                     'contains': purge_check_contains,
                     'from_user': purge_check_from_user,
                     'all': purge_check_always_true}


def has_attachments(min_amount_attachments: int = 1):
    def predicate(ctx):
        if len(ctx.message.attachments) >= min_amount_attachments:
            return True
        else:
            raise MissingAttachmentError(ctx, min_amount_attachments)

    return commands.check(predicate)


def is_not_giddi(ctx):
    if ctx.author.name == 'Giddi':
        return False
    return True


def allowed_channel_and_allowed_role_no_dm(config_name: str, in_dm_allowed: bool = False, allowed_channel_key: str = "allowed_channels", allowed_roles_key: str = "allowed_roles"):
    def predicate(ctx):
        if ctx.bot.is_owner(ctx.bot.creator.member_object):
            log.debug("skipping checks as user is creator/owner: %s", ctx.bot.creator.name)
            return True
        allowed_channels = COGS_CONFIG.getlist(config_name, allowed_channel_key, as_set=True, casefold_items=True)
        allowed_roles = COGS_CONFIG.getlist(config_name, allowed_roles_key, as_set=True, casefold_items=True)
        channel = ctx.channel.name
        channel_type = ctx.channel.type
        roles = ctx.author.roles
        if channel.casefold() not in allowed_channels:
            raise NotAllowedChannelError(ctx, COGS_CONFIG.getlist(config_name, allowed_channel_key))
        if in_dm_allowed is False and channel_type is not discord.ChannelType.text:
            raise IsNotTextChannelError(ctx, channel_type)
        if all(role.name.casefold() not in allowed_roles for role in roles):
            raise NotNecessaryRole(ctx, COGS_CONFIG.getlist(config_name, allowed_roles_key))
        return True
    return commands.check(predicate)

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
