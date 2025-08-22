# cogs/mod.py
import discord
from discord.ext import commands
from datetime import timedelta
import locks

class Mod(commands.Cog):
    def __init__(self, motoko: commands.Bot):
        self.motoko = motoko

    # ban
    @commands.hybrid_command(name='ban', description='ban user (delete messages)')
    @commands.has_permissions(ban_members=True)
    @locks.sync_lock()
    @locks.guild_lock()
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason: str=None):
        await user.ban(reason=reason, delete_message_days=7)
        await ctx.reply(f'{user.mention} was **banned** from **{ctx.guild}**')

    # unban
    @commands.hybrid_command(name='unban', description='unban user')
    @commands.has_permissions(ban_members=True)
    @locks.sync_lock()
    @locks.guild_lock()
    async def unban(self, ctx: commands.Context, user: discord.User, *, reason: str=None):
        await ctx.guild.unban(user, reason=reason)
        await ctx.reply(f'{user.mention} was **unbanned** from **{ctx.guild}**')

    # softban
    @commands.hybrid_command(name='softban', description='softban user (kick & delete messages)')
    @commands.has_permissions(ban_members=True)
    @locks.sync_lock()
    @locks.guild_lock()
    async def softban(self, ctx: commands.Context, user: discord.Member, *, reason: str=None):
        await user.ban(reason=f'[softban] {reason}', delete_message_days=7)
        await user.unban(reason='softban reversal')
        await ctx.reply(f'{user.mention} was **kicked** from **{ctx.guild}**')

    # kick
    @commands.hybrid_command(name='kick', description='kick user (does not delete messages)')
    @commands.has_permissions(ban_members=True)
    @locks.sync_lock()
    @locks.guild_lock()
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str=None):
        await user.kick(reason=reason)
        await ctx.reply(f'{user.mention} was **kicked** from **{ctx.guild}**')

    # mute
    @commands.hybrid_command(name='mute', description='mute user (timeout)')
    @commands.has_permissions(ban_members=True)
    @locks.sync_lock()
    @locks.guild_lock()
    async def mute(self, ctx: commands.Context, user: discord.Member, minutes: int, *, reason: str=None):
        duration = timedelta(minutes=minutes)
        await user.timeout(duration, reason=reason)
        await ctx.reply(f'{user.mention} was **muted** for **{minutes} minutes**')

    # unmute
    @commands.hybrid_command(name='unmute', description='unmute user')
    @commands.has_permissions(ban_members=True)
    @locks.sync_lock()
    @locks.guild_lock()
    async def unmute(self, ctx: commands.Context, user: discord.Member, *, reason: str=None):
        await user.timeout(None, reason=reason)
        await ctx.reply(f'{user.mention} was **unmuted**')

async def setup(motoko: commands.Bot):
    await motoko.add_cog(Mod(motoko))