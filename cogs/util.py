# cogs/util.py
import discord
from discord.ext import commands
from typing import TypeVar, Generic
from datetime import timedelta
import random
import decorators
import fetches

Motoko = TypeVar("Motoko", bound=commands.Bot)

class Util(commands.Cog, Generic[Motoko]):
    def __init__(self, motoko: Motoko):
        self.motoko = motoko

    # help
    @commands.hybrid_command(name='help', aliases=['motoko','commands'], description='return available commands')
    @decorators.sync()
    async def help(self, ctx: commands.Context[Motoko]):
        help = [
            'Prepend commands with:',
            '    /       (slash)',
            '    .       (period)',
            '    @motoko (mention)',
            '\n'
        ]
        for command in self.motoko.tree.get_commands(guild=ctx.guild):
            description = getattr(command, 'description', 'no description')
            help.append(f'{command.name} - {description}')
        help = '\n'.join(help)
        await ctx.reply(f'```{help}```')

    # about
    @commands.hybrid_command(name='about', aliases=['why'], description='return info about motoko')
    @decorators.sync()
    async def about(self, ctx: commands.Context[Motoko]):
        about = [
            'I am a Discord bot inspired by Major Kusanagi from Ghost in the Shell.',
            'Developed by <@234456546715762688> using the discord.py wrapper.',
            'You may add me to your server with this link:',
            'https://discord.com/oauth2/authorize?client_id=1265358841286230016&permissions=0&integration_type=0&scope=bot'
        ]
        await ctx.reply('\n'.join(about))

    # hello
    @commands.hybrid_command(name='hello', aliases=['hi','yo','hey','sup'], description='return a greeting')
    @decorators.sync()
    async def hello(self, ctx: commands.Context[Motoko], *, user: discord.Member | None):
        recipient = user or ctx.author
        greets = [
            'Reporting in',
            'What\'s your status',
            'Good to hear from you',
            'Took you long enough',
            'You\'re clingier than Batou',
            'Get to the point',
            'I read you',
            'Hey there',
            'Yes'
        ]
        await ctx.send(f'{random.choice(greets)} {recipient.mention}')

    # ping
    @commands.hybrid_command(name='ping', aliases=['latency','report'], description='return latency')
    @decorators.sync()
    async def ping(self, ctx: commands.Context[Motoko]):
        latency = round(self.motoko.latency * 1000)
        await ctx.reply(f'I read you with **{latency} ms** of latency')
    
    # cat
    @commands.hybrid_command(name='cat', description='return cat fact')
    @decorators.sync()
    async def cat(self, ctx: commands.Context[Motoko]):
        fact = fetches.Request(None).cat_fact()
        await ctx.reply(fact)

    # time
    @commands.hybrid_command(name='time', aliases=['now'], description='return current time')
    @decorators.sync()
    async def time(self, ctx: commands.Context[Motoko], *, offset: int=0):
        shifted_time = ctx.message.created_at + timedelta(hours=offset)
        offset_str = f'{offset:+03}:00'
        formatted_time = shifted_time.strftime('%b %d, %Y %I:%M %p').replace(' 0', ' ')
        await ctx.reply(f'{formatted_time} {offset_str} (UTC{offset:+})')

    # echo
    @commands.hybrid_command(name='echo', description='return input')
    @decorators.sync()
    async def echo(self, ctx: commands.Context[Motoko], /, input: str):
        await ctx.send(input)

    # user
    @commands.hybrid_command(name='user', aliases=['u','who'], description='return user info')
    @decorators.sync()
    async def user(self, ctx: commands.Context[Motoko], *, user: discord.Member | None):
        target = user or ctx.message.author
        if isinstance(target, discord.Member) and len(target.roles) > 1:
            roles = ' '.join([role.mention for role in target.roles if role.name != '@everyone'])
        else:
            roles = 'user has no role'
        status = target.status if isinstance(target, discord.Member) else "Unknown"
        joined = getattr(target, 'joined_at', None)
        if joined:
            joined_str = joined.strftime('%b %d, %Y %I:%M %p').replace(' 0', ' ')
        else:
            joined_str = 'N/A'
        embed = discord.Embed(title='USER INFORMATION', color=discord.Colour.from_str('#44578e'), timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=target.avatar)
        embed.add_field(name='DISPLAY NAME', inline=False, value=target.mention)
        embed.add_field(name='USERNAME',     inline=False, value=f'`{target.name}`')
        embed.add_field(name='ID',           inline=False, value=target.id)
        embed.add_field(name='STATUS',       inline=False, value=status)
        embed.add_field(name='CREATED',      inline=False, value=target.created_at.strftime('%b %d, %Y %I:%M %p').replace(' 0', ' '))
        embed.add_field(name='JOINED',       inline=False, value=joined_str)
        embed.add_field(name='ROLES',        inline=False, value=roles)
        await ctx.reply(embed=embed)

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Util(motoko))