from discord.ext import commands
import tests

class Test(commands.Cog):
    def __init__(self, motoko: commands.Bot):
        self.motoko = motoko

    def get_testVar(self):
        return tests.testVar

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Test(motoko))