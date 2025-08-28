from discord.ext import commands
from motoko import Motoko
import utils.decorators as decorators
import time

class Tool(commands.Cog):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    # timer
    @commands.hybrid_command(name='timer', aliases=['countdown'], description='return countdown timer for given minutes')
    @decorators.sync()
    async def timer(self, ctx: commands.Context[Motoko], minutes: int):
        now = int(time.time())
        future = now + (minutes * 60)
        timer = f'<t:{future}:R>'
        await ctx.reply(timer)

    # echo
    @commands.hybrid_command(name='echo', description='return input')
    @decorators.sync()
    async def echo(self, ctx: commands.Context[Motoko], *, input: str):
        await ctx.send(input)

async def setup(motoko: Motoko):
    await motoko.add_cog(Tool(motoko))