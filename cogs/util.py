# cogs/util.py
import discord
from discord.ext import commands
from datetime import timedelta
import locks
import json, requests

class Util(commands.Cog):
    def __init__(self, motoko: commands.Bot):
        self.motoko = motoko

    # help
    @commands.hybrid_command(name='help', aliases=['motoko','commands'], description='return available commands')
    @locks.sync_lock()
    @locks.guild_lock()
    async def help(self, ctx: commands.Context):
        help = [
            'Prepend commands with:',
            '    /       (slash)',
            '    .       (period)',
            '    @motoko (mention)',
            '\n'
        ]
        for command in self.motoko.tree.get_commands(guild=ctx.guild):
            help.append(f'{command.name} - {command.description}')
        help = '\n'.join(help)
        await ctx.reply(f'```{help}```')

    # about
    @commands.hybrid_command(name='about', aliases=['why'], description='return info about motoko')
    @locks.sync_lock()
    @locks.guild_lock()
    async def about(self, ctx: commands.Context):
        about = 'I am a Discord bot inspired by Major Motoko Kusanagi from the 1995 animated film Ghost in the Shell. I was developed by <@234456546715762688> using the discord.py wrapper.'
        await ctx.reply(about)

    # hello
    @commands.hybrid_command(name='hello', aliases=['hi','yo','hey','sup'], description='return a greeting')
    @locks.sync_lock()
    @locks.guild_lock()
    async def hello(self, ctx: commands.Context, user: discord.Member=None):
        user = user or ctx.author
        await ctx.send(f'hey there {user.mention} 😏')

    # ping
    @commands.hybrid_command(name='ping', aliases=['latency','report'], description='return latency')
    @locks.sync_lock()
    @locks.guild_lock()
    async def ping(self, ctx: commands.Context):
        latency = round(self.motoko.latency * 1000)
        await ctx.reply(f'I read you with **{latency} ms** of latency')
    
    # cat
    @commands.hybrid_command(name='cat', description='return cat fact')
    @locks.sync_lock()
    @locks.guild_lock()
    async def cat(self, ctx: commands.Context):
        fact = json.loads(requests.get('https://catfact.ninja/fact').text)['fact']
        await ctx.reply(fact)

    # time
    @commands.hybrid_command(name='time', aliases=['now'], description='return current time')
    @locks.sync_lock()
    @locks.guild_lock()
    async def time(self, ctx: commands.Context, offset: int=0):
        shifted_time = ctx.message.created_at + timedelta(hours=offset)
        offset_str = f'{offset:+03}:00'
        formatted_time = shifted_time.strftime('%b %d, %Y %I:%M %p').replace(' 0', ' ')
        await ctx.reply(f'{formatted_time} {offset_str} (UTC{offset:+})')

    # echo
    @commands.hybrid_command(name='echo', description='return input')
    @locks.sync_lock()
    @locks.guild_lock()
    async def echo(self, ctx: commands.Context, *, input: str):
        await ctx.send(input)

    # user
    @commands.hybrid_command(name='user', aliases=['u','who'], description='return user info')
    @locks.sync_lock()
    @locks.guild_lock()
    async def user(self, ctx: commands.Context, user: discord.Member=None):
        user = user or ctx.message.author
        if len(user.roles) > 1:
            roles = ' '.join([role.mention for role in user.roles if role.name != '@everyone'])
        else:
            roles = 'user has no role'
        embed = discord.Embed(title='USER INFORMATION', color=discord.Colour.from_str('#44578e'), timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name='DISPLAY NAME', inline=0, value=f'{user.mention}')
        embed.add_field(name='USERNAME',     inline=0, value=f'`{user.name}`')
        embed.add_field(name='ID',           inline=0, value=user.id)
        embed.add_field(name='STATUS',       inline=0, value=user.status)
        embed.add_field(name='CREATED',      inline=0, value=user.created_at.strftime('%b %d, %Y %I:%M %p').replace(' 0', ' '))
        embed.add_field(name='JOINED',       inline=0, value=user.joined_at.strftime('%b %d, %Y %I:%M %p').replace(' 0', ' '))
        embed.add_field(name='ROLES',        inline=0, value=roles)
        await ctx.reply(embed=embed)

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Util(motoko))