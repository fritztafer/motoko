# cogs/dev.py
import discord
from discord.ext import commands
from typing import Literal, Generic, TypeVar, cast
from importlib import reload
import sys
import decorators
import fetches
import globals

Motoko = TypeVar("Motoko", bound=commands.Bot)

class Dev(commands.Cog, Generic[Motoko]):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    # evaluate
    @commands.hybrid_command(name='eval', description='evaluate input')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def evaluate(self, ctx: commands.Context[Motoko], *, object: str):
        await ctx.reply(f'```{eval(object)}```')

    # sync
    @commands.hybrid_command(name='sync', description='sync command tree')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def synctree(self, ctx: commands.Context[Motoko], server: str | None):
        await ctx.defer()
        if type(server) is type(None):
            if ctx.guild is not None:
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
        elif server is not None and server.isdigit() and int(server) in globals.gids:
            guild = self.motoko.get_guild(int(server))
            if guild is not None:
                synced = await self.motoko.tree.sync(guild=discord.Object(id=guild.id))
                await ctx.reply(f'**{len(synced)} commands** synchronized to **{guild.name}**')
        else:
            await ctx.reply(f'**{server}** is an invalid input')

    # load
    @commands.hybrid_command(name='load', description='load extension')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def load(self, ctx: commands.Context[Motoko], *, cog: str):
        await ctx.defer()
        try:
            await self.motoko.load_extension(f'cogs.{cog}')
            await ctx.reply(f'**{cog}.py** load **success**')
        except Exception as error:
            await ctx.reply(f'**{cog}.py** load **failure**: {error}')

    # unload
    @commands.hybrid_command(name='unload', description='unload extension')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def unload(self, ctx: commands.Context[Motoko], *, cog: str):
        await ctx.defer()
        if cog in ['dev', 'event']:
            await ctx.reply(f'**{cog}.py** cannot be unloaded')
            return
        try:
            await self.motoko.unload_extension(f'cogs.{cog}')
            await ctx.reply(f'**{cog}.py** unload **success**')
        except Exception as error:
            await ctx.reply(f'**{cog}.py** unload **failure**: {error}')

    # reload
    @commands.hybrid_command(name='reload', description='reload extension')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def reload(self, ctx: commands.Context[Motoko], *, cog: str):
        await ctx.defer()
        try:
            await self.motoko.reload_extension(f'cogs.{cog}')
            await ctx.reply(f'**{cog}.py** reload **success**')
        except Exception as error:
            await ctx.reply(f'**{cog}.py** reload **failure**: {error}')

    # module
    @commands.hybrid_command(name='module', description='reload module')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def module(self, ctx: commands.Context[Motoko], *, name: str):
        try:
            if name in sys.modules:
                module = sys.modules[name]
                reload(module)
            await ctx.reply(f'**{name}.py** reload **success**')
        except Exception as error:
            await ctx.reply(f'**{name}.py** reload **failure**: {error}')

    # conf_read
    @commands.hybrid_command(name='conf_read', description='read from configuration file')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def conf_read(self, ctx: commands.Context[Motoko], object: Literal['developer','blacklist'], list: Literal['users','guilds']):
        try:
            object_literal = cast(Literal['DEVELOPER', 'BLACKLIST'], object.upper())
            list_literal = cast(Literal['USERS', 'GUILDS'], list.upper())
            result = fetches.Config().read(object_literal, list_literal)
            await ctx.reply(f'{object} {list}: {result}')
        except Exception as error:
            await ctx.reply(f'could not fetch {object} {list}: {error}')

    # conf_write
    @commands.hybrid_command(name='conf_write', description='write to configuration file')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def conf_write(self, ctx: commands.Context[Motoko], action: Literal['add','del'], object: Literal['developer','blacklist'], list: Literal['users','guilds'], id: str):
        try:
            id_int: int = int(id)
            object_literal = cast(Literal['DEVELOPER', 'BLACKLIST'], object.upper())
            list_literal = cast(Literal['USERS', 'GUILDS'], list.upper())
            result = 'added to' if action == 'add' else 'deleted from'
            fetches.Config().write(action, object_literal, list_literal, id_int)
            if id_int in globals.gids:
                guild = self.motoko.get_guild(id_int)
                if guild:
                    await guild.leave()
            await ctx.reply(f'{id} {result} {object} {list}')
        except Exception as error:
            await ctx.reply(f'{id} could not be {object} {list}: {error}')

    # joined
    @commands.hybrid_command(name='joined', description='return information about joined servers')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def joined(self, ctx: commands.Context[Motoko]):
        servers = ''
        for id in globals.gids:
            guild = self.motoko.get_guild(id)
            if guild:
                servers += '\n' + guild.name + ': ' + str(guild.id)
        await ctx.reply(f'Member of **{len(globals.gids)} servers**:```{servers}```')

    # leave
    @commands.hybrid_command(name='leave', description='leave given server')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def leave(self, ctx: commands.Context[Motoko], *, id: str):
        guild = self.motoko.get_guild(int(id))
        if guild:
            await guild.leave()
            await ctx.reply(f'Left `{guild.name}`')
        else:
            await ctx.reply(f'{id} is invalid')

    # shutdown
    @commands.hybrid_command(name='shutdown', description='terminate bot processes')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def shutdown(self, ctx: commands.Context[Motoko]):
        await ctx.reply('Affirmative, **shutdown** initiated')
        await self.motoko.close()

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Dev(motoko))