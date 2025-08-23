# locks.py
import discord
from discord.ext import commands
from discord import app_commands
import fetches, globals

# lock to dev guilds & users
def dev_lock():
    def predicate(ctx: discord.Interaction):
        if ctx.guild.id in fetches.Config().dev_guilds():
            if ctx.message.author.id in fetches.Config().dev_users():
                return True
    return commands.check(predicate)

# lock to dev guilds in tree.sync()
def dev_sync():
    return app_commands.guilds(*fetches.Config().dev_guilds())

# lock to joined guilds in tree.sync()
def sync():
    return app_commands.guilds(*globals.gids)