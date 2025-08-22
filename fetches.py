from discord.ext import commands
import json

class Config:
    def __init__(self):
        with open('./config.json', 'r') as f:
            self.config = json.load(f)

    def fetch_token(self):
        return self.config['TOKEN']

    def fetch_dev_users(self):
        return self.config['DEVELOPERS']['USERS']

    def fetch_dev_guilds(self):
        return self.config['DEVELOPERS']['GUILDS']

class Motoko(commands.Bot):
    def __init__():
        pass

    async def fetch_guild_ids(self):
        return [guild.id async for guild in self.fetch_guilds(limit=None, with_counts=False)]