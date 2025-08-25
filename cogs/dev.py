# cogs/dev.py
import discord
from discord.ext import commands
from motoko import Motoko
import util.decorators as decorators
from util.fetches import config
from states import state
from typing import Literal, cast
from importlib import reload, import_module
import sys

class Dev(commands.Cog):
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
        guild_ids: list[int] = [guild.id for guild in self.motoko.guilds]
        if type(server) is type(None):
            if ctx.guild:
                synced = await self.motoko.tree.sync(guild=discord.Object(id=ctx.guild.id))
                await ctx.reply(f'**{len(synced)} commands** synchronized to **{ctx.guild}**')
            return
        if str(server) == 'all':
            for guild in guild_ids:
                if guild_ids.index(guild) < len(guild_ids)-1:
                    await self.motoko.tree.sync(guild=discord.Object(id=guild))
                else:
                    await self.motoko.tree.sync(guild=discord.Object(id=guild))
                    await ctx.reply(f'Command tree synchronized to **{len(guild_ids)} servers**')
        elif server and server.isdigit() and int(server) in guild_ids:
            guild = self.motoko.get_guild(int(server))
            if guild:
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
        await ctx.defer()
        if name == 'states':
            await ctx.reply(f'**{name}.py** cannot be reloaded')
            return
        try:
            if name not in sys.modules:
                module = import_module(name)
            else:
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
            result = config.read(object_literal, list_literal)
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
            config.write(action, object_literal, list_literal, id_int)
            if action == 'add':
                if object == 'developer':
                    if list == 'users':
                        state.add_dev_user(id_int)
                    elif list == 'guilds':
                        state.add_dev_guild(id_int)
                elif object == 'blacklist':
                    if list == 'users':
                        state.add_ban_user(id_int)
                    elif list == 'guilds':
                        state.add_ban_guild(id_int)
            elif action == 'del':
                if object == 'developer':
                    if list == 'users':
                        state.del_dev_user(id_int)
                    elif list == 'guilds':
                        state.del_dev_guild(id_int)
                elif object == 'blacklist':
                    if list == 'users':
                        state.del_ban_user(id_int)
                    elif list == 'guilds':
                        state.del_ban_guild(id_int)
            if action == 'add' and object == 'blacklist' and list == 'guilds':
                if id_int in [guild.id for guild in self.motoko.guilds]:
                    guild = self.motoko.get_guild(id_int)
                    await guild.leave() if guild else guild
            await ctx.reply(f'{id} {result} {object} {list}')
        except Exception as error:
            await ctx.reply(f'{id} could not be {object} {list}: {error}')

    # joined
    @commands.hybrid_command(name='joined', description='return information about joined servers')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def joined(self, ctx: commands.Context[Motoko]):
        servers = ''
        for guild in self.motoko.guilds:
            servers += '\n' + guild.name + ': ' + str(guild.id)
        await ctx.reply(f'Member of **{len(self.motoko.guilds)} servers**:```{servers}```')

    # leave
    @commands.hybrid_command(name='leave', description='leave given server')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def leave(self, ctx: commands.Context[Motoko], *, id: str):
        guild = self.motoko.get_guild(int(id))
        if guild:
            await guild.leave()
            await ctx.reply(f'`{guild.name}` left successfully')
        else:
            await ctx.reply(f'{id} is invalid')

    # shutdown
    @commands.hybrid_command(name='shutdown', description='terminate bot processes')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def shutdown(self, ctx: commands.Context[Motoko]):
        await ctx.reply('Affirmative, **shutdown** initiated')
        await self.motoko.shutdown()

    # restart
    @commands.hybrid_command(name='restart', description='restart bot processes')
    @decorators.dev_lock()
    @decorators.dev_sync()
    async def restart(self, ctx: commands.Context[Motoko]):
        await ctx.reply('Affirmative, **restart** initiated')
        await self.motoko.restart()

async def setup(motoko: Motoko):
    await motoko.add_cog(Dev(motoko))