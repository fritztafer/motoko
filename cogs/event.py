# cogs/event.py
import discord
from discord.ext import commands
import globals

class Event(commands.Cog):
    def __init__(self, motoko: commands.Bot):
        self.motoko = motoko

    # join server
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        globals.gids.append(guild.id)
        await self.motoko.tree.sync(guild=guild)

    # leave server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        globals.gids.remove(guild.id)
    
    # error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        original = getattr(error, "original", error)
        if isinstance(original, commands.MissingPermissions):
            await ctx.reply("denied")
        elif isinstance(original, commands.BadArgument):
            await ctx.reply("invalid")
        elif isinstance(original, discord.Forbidden):
            await ctx.reply("forbidden")
        elif isinstance(original, discord.NotFound):
            await ctx.reply("not found")
        else:
            # await ctx.reply(f"unexpected: `{type(original).__name__}`")
            raise error

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Event(motoko))