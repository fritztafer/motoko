# cogs/dev.py
import discord
from discord.ext import commands
import locks, globals

class Dev(commands.Cog):
    def __init__(self, motoko: commands.Bot):
        self.motoko = motoko

    # evaluate
    @commands.hybrid_command(name='eval', description='evaluate input')
    @locks.dev_user_lock()
    @locks.dev_guild_lock()
    @locks.dev_sync_lock()
    async def evaluate(self, ctx: commands.Context, *, object: str):
        await ctx.reply(f'```{eval(object)}```')

    # sync
    @commands.hybrid_command(name='sync', description='sync command tree')
    @locks.dev_user_lock()
    @locks.dev_guild_lock()
    @locks.dev_sync_lock()
    async def synctree(self, ctx: commands.Context, server: str=None):
        await ctx.defer()
        if type(server) is type(None):
            synced = await self.motoko.tree.sync(guild=discord.Object(id=ctx.guild.id))
            await ctx.reply(f'**{len(synced)} commands** synchronized to **{ctx.guild}**')
            return
        if str(server) == 'all':
            for guild in globals.gids:
                if globals.gids.index(guild) < len(globals.gids)-1:
                    await self.motoko.tree.sync(guild=discord.Object(id=guild))
                else:
                    await self.motoko.tree.sync(guild=discord.Object(id=guild))
                    await ctx.reply(f'Command tree synchronized to **{len(globals.gids)} servers**')
        elif server.isdigit() and int(server) in globals.gids:
            synced = await self.motoko.tree.sync(guild=discord.Object(id=int(server))) 
            await ctx.reply(f'**{len(synced)} commands** synchronized to **{self.motoko.get_guild(int(server)).name}**')
        else:
            await ctx.reply(f'**{server}** is an invalid input')

    # load
    @commands.hybrid_command(name='load', description='load extension')
    @locks.dev_user_lock()
    @locks.dev_guild_lock()
    @locks.dev_sync_lock()
    async def load(self, ctx: commands.Context, cog: str):
        await ctx.defer()
        try:
            await self.motoko.load_extension(f'cogs.{cog}')
            await ctx.reply(f'**{cog}.py** load **success**')
        except: 
            await ctx.reply(f'**{cog}.py** load **failure**')

    # unload
    @commands.hybrid_command(name='unload', description='unload extension')
    @locks.dev_user_lock()
    @locks.dev_guild_lock()
    @locks.dev_sync_lock()
    async def unload(self, ctx: commands.Context, cog: str):
        await ctx.defer()
        if cog in ['dev', 'event']:
            await ctx.reply(f'**{cog}.py** cannot be unloaded')
            return
        try:
            await self.motoko.unload_extension(f'cogs.{cog}')
            await ctx.reply(f'**{cog}.py** unload **success**')
        except: 
            await ctx.reply(f'**{cog}.py** unload **failure**')

    # reload
    @commands.hybrid_command(name='reload', description='reload extension')
    @locks.dev_user_lock()
    @locks.dev_guild_lock()
    @locks.dev_sync_lock()
    async def reload(self, ctx: commands.Context, cog: str):
        await ctx.defer()
        try:
            await self.motoko.reload_extension(f'cogs.{cog}')
            await ctx.reply(f'**{cog}.py** reload **success**')
        except: 
            await ctx.reply(f'**{cog}.py** reload **failure**')
    
    # joined
    @commands.hybrid_command(name='joined', description='return information about joined servers')
    @locks.dev_user_lock()
    @locks.dev_guild_lock()
    @locks.dev_sync_lock()
    async def joined(self, ctx: commands.Context):
        count = 0
        servers = ''
        for id in globals.gids:
            count += 1
            servers += '\n' + self.motoko.get_guild(int(id)).name + ': ' + str(id)
        await ctx.reply(f'Currently a member of **{count} servers**:```{servers}```')

    # shutdown
    @commands.hybrid_command(name='shutdown', description='terminate bot processes')
    @locks.dev_user_lock()
    @locks.dev_guild_lock()
    @locks.dev_sync_lock()
    async def shutdown(self, ctx: commands.Context):
        await ctx.reply('Affirmative, **shutdown** initiated')
        await self.motoko.close()

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Dev(motoko))