from discord.ext import commands
from motoko import Motoko
import util.decorators as decorators
from util.fetches import request

class Req(commands.Cog):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    # catf
    @commands.hybrid_command(name='catf', description='return cat fact')
    @decorators.sync()
    async def cat_fact(self, ctx: commands.Context[Motoko]):
        fact = request.cat_fact()
        await ctx.reply(fact)

    # catp
    @commands.hybrid_command(name='catp', description='return cat picture')
    @decorators.sync()
    async def cat_pic(self, ctx: commands.Context[Motoko]):
        fact = request.cat_pic()
        await ctx.reply(fact)

    # define
    @commands.hybrid_command(name='define', description='define given word')
    @decorators.sync()
    async def define(self, ctx: commands.Context[Motoko], word: str):
        definition = request.define(word)
        await ctx.reply(definition)

    # quote
    @commands.hybrid_command(name='quote', description='return a quote')
    @decorators.sync()
    async def quote(self, ctx: commands.Context[Motoko]):
        quote = request.quote()
        await ctx.reply(quote)

async def setup(motoko: Motoko):
    await motoko.add_cog(Req(motoko))