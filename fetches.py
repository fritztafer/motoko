from typing import Literal
import json
import requests

class Config:
    def __init__(self):
        with open('./config.json', 'r') as file:
            self.config = json.load(file)

    def token(self):
        return self.config['TOKEN']

    def dev_users(self):
        return self.config['DEVELOPER']['USERS']

    def dev_guilds(self):
        return self.config['DEVELOPER']['GUILDS']
    
    def blacklist_users(self):
        return self.config['BLACKLIST']['USERS']

    def blacklist_guilds(self):
        return self.config['BLACKLIST']['GUILDS']

    def read(self, object: Literal['DEVELOPER','BLACKLIST'], list: Literal['USERS','GUILDS']):
        self.list = self.config[object][list]
        return self.list

    def write(self, action: Literal['add','del'], object: Literal['DEVELOPER','BLACKLIST'], list: Literal['USERS','GUILDS'], id: int):
        self.action = action
        self.list = self.config[object][list]
        self.id = id
        if self.action == 'add':
            if self.id not in self.list:
                self.list.append(self.id)                
        elif self.action == 'del':
            if self.id in self.list:
                self.list.remove(self.id)
        with open('./config.json', 'w') as file:
            json.dump(self.config, file, indent=4)

class Request:
    def __init__(self, url: str | None):
        self.url = url
    
    def cat_fact(self):
        return json.loads(requests.get('https://catfact.ninja/fact').text)['fact']