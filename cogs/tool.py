from discord.ext import commands
from motoko import Motoko
import utils.decorators as decorators
from typing import Literal
from datetime import datetime
from zoneinfo import ZoneInfo
import time

class Tool(commands.Cog):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    # time
    @commands.hybrid_command(name='time', aliases=['now'], description='return current time')
    @decorators.sync()
    async def time(self, ctx: commands.Context[Motoko], timezone: Literal['US/Pacific','US/Mountain','US/Central','US/Eastern','US/Hawaii','US/Alaska','Brazil/East','Europe/London','Europe/Berlin','Europe/Moscow','Asia/Dubai','Asia/Singapore','Asia/Shanghai','Asia/Tokyo','Australia/Sydney','Pacific/Auckland']):
        try:
            tz = ZoneInfo(timezone)
            local_time = datetime.now(tz)
            formatted = local_time.strftime('%B %d, %Y %I:%M %p').replace(' 0', ' ')
            abbr = local_time.tzname()
            offset = local_time.utcoffset()
            if offset:
                hours = int(offset.total_seconds() // 3600)
                minutes = int((offset.total_seconds() % 3600) // 60)
                offset_str = f"{hours:+03}:{minutes:02}"
            else:
                offset_str = ''
            message = f'{formatted} {abbr} ({offset_str} UTC)'
        except Exception:
            message = 'Missing timezone data.'
        await ctx.reply(message)

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