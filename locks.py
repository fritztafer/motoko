# locks.py
import discord
from discord.ext import commands
from discord import app_commands
import fetches, globals

# lock to dev users
def dev_user_lock():
    def predicate(ctx: discord.Interaction):
        if ctx.message.author.id in fetches.Config().fetch_dev_users():
            return True
    return commands.check(predicate)

# lock to dev guilds
def dev_guild_lock():
    def predicate(ctx: discord.Interaction):
        if ctx.guild.id in fetches.Config().fetch_dev_guilds():
            return True
    return commands.check(predicate)

# disable direct message commands
def guild_lock():
    def predicate(ctx: commands.Context):
        if ctx.guild is not None or ctx.author.id in fetches.Config().fetch_dev_users():
            return True
    return commands.check(predicate)

# lock to dev guilds in tree.sync()
def dev_sync_lock():
    return app_commands.guilds(*fetches.Config().fetch_dev_guilds())

# lock to given guilds in tree.sync()
def sync_lock():
    return app_commands.guilds(*globals.gids)