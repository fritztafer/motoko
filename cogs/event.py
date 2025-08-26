import discord
from discord.ext import commands
from motoko import Motoko
from states import state
from util.logs import logger

class Event(commands.Cog):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    # join server
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        logger.info('join server ' + guild.name)
        if guild.id in state.ban_guilds:
            await guild.leave()
            return
        state.add_all_guild(guild.id)
        await self.motoko.tree.sync(guild=guild)

    # leave server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        logger.info('left server ' + guild.name)
        state.del_all_guild(guild.id)

async def setup(motoko: Motoko):
    await motoko.add_cog(Event(motoko))