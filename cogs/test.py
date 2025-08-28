from discord.ext import commands
from motoko import Motoko
import utils.tests as tests
import utils.decorators as decorators

class Test(commands.Cog):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko
        self.tests = tests

    @commands.hybrid_command(name='test', description='test command')
    @decorators.dev_lock()
    @decorators.sync(dev=True)
    async def test(self, ctx: commands.Context[Motoko]):
        await ctx.reply("test " + str(123) + self.tests.testVar)

async def setup(motoko: Motoko):
    await motoko.add_cog(Test(motoko))