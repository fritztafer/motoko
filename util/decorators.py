from discord.ext import commands
from discord import app_commands
from motoko import Motoko
from state import state

# lock to dev users & guilds
def dev_lock():
    def predicate(ctx: commands.Context[Motoko]) -> bool:
        if ctx.message and ctx.message.author.id in state.dev_users:
            if ctx.guild and ctx.guild.id in state.dev_guilds:
                return True
        return False
    return commands.check(predicate)

# lock to given guilds in tree.sync()
def sync(dev: bool=False):
    if dev or state.testing:
        guilds = state.dev_guilds
    else:
        guilds = state.all_guilds
    return app_commands.guilds(*guilds)