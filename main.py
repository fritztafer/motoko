# main.py
import discord
from discord.ext import commands
from discord import app_commands
import logging, logging.handlers
import asyncio
import os
import fetches, globals

class Motoko(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        globals.gids = [guild.id async for guild in self.fetch_guilds(limit=None, with_counts=False)]
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')
        print(f'Major logged into Discord as {self.user} connected to {len(globals.gids)} servers')

        interaction_check = self.tree.interaction_check
        async def on_interaction(ctx: discord.Interaction):
            if ctx.guild_id in fetches.Config().blacklist_guilds(): return await self.get_guild(ctx.guild_id).leave()
            if ctx.user.id in fetches.Config().blacklist_users(): return
            return await interaction_check(ctx)
        self.tree.interaction_check = on_interaction

    async def on_message(self, ctx: discord.Message):
        if ctx.guild.id in fetches.Config().blacklist_guilds(): return await self.get_guild(ctx.guild.id).leave()
        if ctx.author.id in fetches.Config().blacklist_users(): return
        if isinstance(ctx.channel, discord.DMChannel): return
        if ctx.author.bot: return
        await self.process_commands(ctx)
    
    async def on_command_error(self, ctx, error):
        if hasattr(ctx, 'interaction') and ctx.interaction: # slash command
            original = getattr(error, 'original', error)
            if isinstance(error, commands.HybridCommandError): # hybrid command errors - unwrap twice
                original = getattr(error.original, 'original', error.original)
            if isinstance(original, (commands.MissingPermissions, app_commands.MissingPermissions)):
                await ctx.reply('denied')
            elif isinstance(original, (commands.BadArgument, app_commands.TransformerError)):
                await ctx.reply('invalid')
            elif isinstance(original, discord.Forbidden):
                await ctx.reply('forbidden')
            elif isinstance(original, discord.NotFound):
                await ctx.reply('not found')
            else:
                raise error
        else: # text command
            original = getattr(error, 'original', error)
            if isinstance(original, commands.MissingPermissions):
                await ctx.reply('denied')
            elif isinstance(original, commands.BadArgument):
                await ctx.reply('invalid')
            elif isinstance(original, discord.Forbidden):
                await ctx.reply('forbidden')
            elif isinstance(original, discord.NotFound):
                await ctx.reply('not found')
            else:
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