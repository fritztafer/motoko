# main.py
import discord
from discord.ext import commands
from discord import app_commands
from states import state
from util.fetches import config
from util.logs import logger, motoko_log, log_command
from typing import Any
import asyncio
import os
import sys

class Motoko(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        state.all_guilds = [guild.id async for guild in self.fetch_guilds(limit=None, with_counts=False)]
        state.ban_guilds = config.ban_guilds()
        state.ban_users = config.ban_users()
        state.dev_guilds = config.dev_guilds()
        state.dev_users = config.dev_users()
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')

        async def on_interaction(ctx: discord.Interaction[Any]):
            guild = self.get_guild(ctx.guild.id) if ctx.guild is not None else None
            if guild and guild.id in state.ban_guilds:
                await guild.leave()
                return False
            if ctx.user.id in state.ban_users: 
                return False
            return await interaction_check(ctx)
        interaction_check = self.tree.interaction_check
        self.tree.interaction_check = on_interaction

    async def on_message(self, ctx: discord.Message):
        guild = self.get_guild(ctx.guild.id) if ctx.guild is not None else None
        if guild and guild.id in state.ban_guilds:
            await guild.leave()
            return
        if ctx.author.id in state.ban_users:
            return
        if isinstance(ctx.channel, discord.DMChannel):
            return
        await self.process_commands(ctx)

    async def on_command_completion(self, ctx: commands.Context[Any]):
        log_command(ctx)

    async def on_command_error(self, ctx: commands.Context[Any], error: Exception):
        original = getattr(error, 'original', error)
        if isinstance(error, commands.HybridCommandError):
            original = getattr(error.original, 'original', error.original)
        error_map: dict[type[BaseException], str] = {
            commands.BadArgument: 'invalid',
            app_commands.TransformerError: 'invalid',
            commands.MissingPermissions: 'denied',
            app_commands.MissingPermissions: 'denied',
            discord.Forbidden: 'forbidden',
            discord.NotFound: 'not found',
        }
        for err_type, message in error_map.items():
            if isinstance(original, err_type):
                await ctx.reply(message)
                return
        raise error

    async def on_ready(self):
        logger.info('ready')
        print(f'{self.user} connected to {len(self.guilds)} servers')

    async def shutdown(self):
        logger.info('shutdown initiated')
        await self.close()

    async def restart(self):
        logger.info('restart initiated')
        await self.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)

async def motoko():
    motoko_log()
    logger.info('startup initiated')

    TOKEN = config.token()

    async with Motoko(
        command_prefix=commands.when_mentioned_or('.'),
        intents=discord.Intents.all(), 
        help_command=None,
    ) as motoko:
        await motoko.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(motoko())