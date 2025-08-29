from discord.ext import commands
from motoko import Motoko
import utils.decorators as decorators
from utils.fetches import request

class Req(commands.Cog):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    # cat
    @commands.hybrid_command(name='cat', description='return cat picture')
    @decorators.sync()
    async def cat(self, ctx: commands.Context[Motoko]):
        response = request('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            response = response.json()[0]
            message = response['url']
        else:
            message = 'https://media.tenor.com/JjVEMUm8yigAAAAM/no-cat.gif'
        await ctx.reply(message)

    # define
    @commands.hybrid_command(name='define', description='define given word')
    @decorators.sync()
    async def define(self, ctx: commands.Context[Motoko], word: str):
        response = request(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        if response.status_code == 200:
            response = response.json()[0]
            definitions = response['word']
            for meaning in response['meanings']:
                definitions += '\n' + meaning['partOfSpeech'] + ': ' + meaning['definitions'][0]['definition']
            message = definitions
        else:
            message = word + ' not found'
        await ctx.reply(message)

    # quote
    @commands.hybrid_command(name='quote', description='return a quote')
    @decorators.sync()
    async def quote(self, ctx: commands.Context[Motoko]):
        response = request('https://zenquotes.io/api/random')
        if response.status_code == 200:
            response = response.json()[0]
            quote = response['q']
            author = response['a']
            message = '"' + quote + '"\n**' + author + '**'
        else:
            message = '"The only quote currently available is this one."\n**Fritz**'
        await ctx.reply(message)

async def setup(motoko: Motoko):
    await motoko.add_cog(Req(motoko))