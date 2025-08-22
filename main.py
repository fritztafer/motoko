# main.py
import discord
from discord.ext import commands
import logging
import logging.handlers
import asyncio
import os
import fetches, globals

class Motoko(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        globals.gids = await fetches.Motoko.fetch_guild_ids(self)
        for f in os.listdir('./cogs'):
            if f.endswith('.py'):
                await self.load_extension(f'cogs.{f[:-3]}')
        print(f'Major logged into Discord as {self.user} connected to {len(globals.gids)} servers')

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

    TOKEN = fetches.Config().fetch_token()

    async with Motoko(
        command_prefix=commands.when_mentioned_or('.'),
        intents=discord.Intents.all(), 
        help_command=None,
    ) as motoko:
        await motoko.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())