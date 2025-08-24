from discord.ext import commands
from typing import TypeVar, Generic
import tests

Motoko = TypeVar("Motoko", bound=commands.Bot)

class Test(commands.Cog, Generic[Motoko]):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    def get_testVar(self):
        return tests.testVar

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Test(motoko))