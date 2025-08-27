from typing import Literal, List
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

    def read(self, object: Literal['DEVELOPER','BLACKLIST'], list: Literal['USERS','GUILDS']) -> list[int]:
        self.list = self.config[object][list]
        return self.list

    def write(self, action: Literal['add','del'], object: Literal['DEVELOPER','BLACKLIST'], list: Literal['USERS','GUILDS'], id: int):
        self.action = action
        self.list: List[int] = self.config[object][list]
        self.id = id
        if self.action == 'add':
            if self.id not in self.list:
                self.list.append(self.id)                
        elif self.action == 'del':
            if self.id in self.list:
                self.list.remove(self.id)
        with open('./config.json', 'w') as file:
            json.dump(self.config, file, indent=4)

config = Config()

def request(url: str) -> requests.Response:
    return requests.get(url)