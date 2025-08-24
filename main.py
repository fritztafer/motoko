# main.py
import discord
from discord.ext import commands
from discord import app_commands
from typing import Any
import logging
import logging.handlers
import asyncio
import os
import fetches
import globals

class Motoko(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        globals.gids = [guild.id async for guild in self.fetch_guilds(limit=None, with_counts=False)]
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')
        print(f'Major logged into Discord as {self.user} connected to {len(globals.gids)} servers')

        interaction_check = self.tree.interaction_check
        async def on_interaction(ctx: discord.Interaction):
            guild = self.get_guild(ctx.guild.id) if ctx.guild is not None else None
            if guild and guild.id in fetches.Config().blacklist_guilds():
                await guild.leave()
                return False
            if ctx.user.id in fetches.Config().blacklist_users(): 
                return False
            return await interaction_check(ctx) # type: ignore
        self.tree.interaction_check = on_interaction

    async def on_message(self, ctx: discord.Message):
        guild = self.get_guild(ctx.guild.id) if ctx.guild is not None else None
        if guild and guild.id in fetches.Config().blacklist_guilds():
            await guild.leave()
            return
        if ctx.author.id in fetches.Config().blacklist_users():
            return
        if isinstance(ctx.channel, discord.DMChannel):
            return
        if ctx.author.bot:
            return
        await self.process_commands(ctx)
    
    async def on_command_error(self, ctx: commands.Context[Any], error: Exception):
        original = getattr(error, "original", error)
        if isinstance(error, commands.HybridCommandError):
            original = getattr(error.original, "original", error.original)
        error_map: dict[type[BaseException], str] = {
            commands.MissingPermissions: "denied",
            commands.BadArgument: "invalid",
            app_commands.MissingPermissions: "denied",
            app_commands.TransformerError: "invalid",
            discord.Forbidden: "forbidden",
            discord.NotFound: "not found",
        }
        for err_type, message in error_map.items():
            if isinstance(original, err_type):
                await ctx.reply(message)
                return
        raise error

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename='motoko.log',
        encoding='utf-8',
        maxBytes=1*1024*1024,
        backupCount=1,
    )
    datetime_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname}] {name}: {message}', datetime_format, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    TOKEN = fetches.Config().token()
    async with Motoko(
        command_prefix=commands.when_mentioned_or('.'),
        intents=discord.Intents.all(), 
        help_command=None,
    ) as motoko:
        await motoko.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())