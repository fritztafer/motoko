# cogs/util.py
import discord
from discord.ext import commands
import decorators, fetches
from datetime import timedelta
import random

class Util(commands.Cog):
    def __init__(self, motoko: commands.Bot):
        self.motoko = motoko

    # help
    @commands.hybrid_command(name='help', aliases=['motoko','commands'], description='return available commands')
    @decorators.sync()
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
    @decorators.sync()
    async def about(self, ctx: commands.Context):
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
    async def hello(self, ctx: commands.Context, user: discord.Member=None):
        user = user or ctx.author
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
        await ctx.send(f'{random.choice(greets)} {user.mention}')

    # ping
    @commands.hybrid_command(name='ping', aliases=['latency','report'], description='return latency')
    @decorators.sync()
    async def ping(self, ctx: commands.Context):
        latency = round(self.motoko.latency * 1000)
        await ctx.reply(f'I read you with **{latency} ms** of latency')
    
    # cat
    @commands.hybrid_command(name='cat', description='return cat fact')
    @decorators.sync()
    async def cat(self, ctx: commands.Context):
        fact = fetches.Request().cat_fact()
        await ctx.reply(fact)

    # time
    @commands.hybrid_command(name='time', aliases=['now'], description='return current time')
    @decorators.sync()
    async def time(self, ctx: commands.Context, offset: int=0):
        shifted_time = ctx.message.created_at + timedelta(hours=offset)
        offset_str = f'{offset:+03}:00'
        formatted_time = shifted_time.strftime('%b %d, %Y %I:%M %p').replace(' 0', ' ')
        await ctx.reply(f'{formatted_time} {offset_str} (UTC{offset:+})')

    # echo
    @commands.hybrid_command(name='echo', description='return input')
    @decorators.sync()
    async def echo(self, ctx: commands.Context, *, input: str):
        await ctx.send(input)

    # user
    @commands.hybrid_command(name='user', aliases=['u','who'], description='return user info')
    @decorators.sync()
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