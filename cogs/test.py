from discord.ext import commands
from motoko import Motoko
import util.tests as tests
import util.decorators as decorators

class Test(commands.Cog):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    @commands.hybrid_command(name='test', description='test command')
    @decorators.dev_lock()
    @decorators.sync(dev=True)
    async def test(self, ctx: commands.Context[Motoko]):
        await ctx.reply("test " + str(123) + Test.get_testVar(self))

    def get_testVar(self) -> str:
        return tests.testVar

async def setup(motoko: Motoko):
    await motoko.add_cog(Test(motoko))