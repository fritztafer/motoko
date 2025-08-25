from typing import Literal, List
import json
import requests

class Config:
    def __init__(self):
        with open('./config.json', 'r') as file:
            self.config = json.load(file)

    def token(self) -> str:
        return self.config['TOKEN']

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

class Request:
    def __init__(self, url: str):
        self.url = url

    def cat_fact(self) -> str:
        try:
            response = requests.get('https://catfact.ninja/fact').json()['fact']
        except Exception:
            return 'unavailable'
        return response

    def cat_pic(self) -> str:
        try:
            response = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
        except Exception:
            return 'unavailable'
        return response

    def define(self, word: str) -> str:
        try:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()[0]
        except Exception:
            return word + ' not found'
        definitions = response['word']
        for meaning in response['meanings']:
            definitions += '\n' + meaning['partOfSpeech'] + ': ' + meaning['definitions'][0]['definition']
        return definitions
    
    def quote(self) -> str:
        try:
            response = requests.get('https://zenquotes.io/api/random').json()[0]
        except Exception:
            return 'unavailable'
        return '"' + response['q'] + '"\n**' + response['a'] + '**'

config = Config()
request = Request(url="")