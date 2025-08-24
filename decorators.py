# locks.py
from discord.ext import commands
from discord import app_commands
from typing import TypeVar
import fetches
import globals

Motoko = TypeVar("Motoko", bound=commands.Bot)

# lock to dev guilds & users
def dev_lock():
    def predicate(ctx: commands.Context[Motoko]) -> bool:
        if ctx.guild and ctx.guild.id in fetches.Config().dev_guilds():
            if ctx.message and ctx.message.author.id in fetches.Config().dev_users():
                return True
        return False
    return commands.check(predicate)

# lock to dev guilds in tree.sync()
def dev_sync():
    return app_commands.guilds(*fetches.Config().dev_guilds())

# lock to joined guilds in tree.sync()
def sync():
    return app_commands.guilds(*globals.gids)