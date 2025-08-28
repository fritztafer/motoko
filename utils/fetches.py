import json
import requests

class Config:
    def __init__(self):
        with open('./config.json', 'r') as file:
            self.config = json.load(file)

    def token(self) -> str:
        return self.config['TOKEN']

    def prefix(self) -> str:
        return self.config['PREFIX']

    def testing(self) -> int:
        return self.config['TESTING']

    def dev_users(self) -> list[int]:
        return self.config['DEVELOPER']['USERS']

    def dev_guilds(self) -> list[int]:
        return self.config['DEVELOPER']['GUILDS']
    
    def ban_users(self) -> list[int]:
        return self.config['BLACKLIST']['USERS']

    def ban_guilds(self) -> list[int]:
        return self.config['BLACKLIST']['GUILDS']

config = Config()

def request(url: str) -> requests.Response:
    return requests.get(url)