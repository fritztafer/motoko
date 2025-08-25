# decorators.py
from discord.ext import commands
from discord import app_commands
from motoko import Motoko
from states import state

# lock to dev users & guilds
def dev_lock():
    def predicate(ctx: commands.Context[Motoko]) -> bool:
        if ctx.message and ctx.message.author.id in state.dev_users:
            if ctx.guild and ctx.guild.id in state.dev_guilds:
                return True
        return False
    return commands.check(predicate)

# lock to dev guilds in tree.sync()
def dev_sync():
    return app_commands.guilds(*state.dev_guilds)

# lock to all guilds in tree.sync()
def sync():
    return app_commands.guilds(*state.all_guilds)