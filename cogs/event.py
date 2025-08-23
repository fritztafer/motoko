# cogs/event.py
import discord
from discord.ext import commands
import fetches, globals

class Event(commands.Cog):
    def __init__(self, motoko: commands.Bot):
        self.motoko = motoko

    # join server
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if guild.id in fetches.Config().blacklist_guilds():
            await guild.leave()
            return
        globals.gids.append(guild.id)
        await self.motoko.tree.sync(guild=guild)

    # leave server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        globals.gids.remove(guild.id)

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Event(motoko))