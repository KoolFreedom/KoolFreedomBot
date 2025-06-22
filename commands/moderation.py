import discord
import os
import json
import asyncio
import re
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Context
from checks import is_discord_staff

WARNINGS_FILE = "data/warnings.json"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped_messages = {}

    def build_embed(self, title, description, color=discord.Color.blue()):
        return discord.Embed(title=title, description=description, color=color)

    def load_warnings():
        if not os.path.exists(WARNINGS_FILE):
            return {}
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)

    def save_warnings(data):
        with open(WARNINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
    
    def parse_time(time_str: str) -> int:
        """
        Parses a string like '10s', '5m', '2h', or '1d' into seconds.
        """
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        match = re.fullmatch(r"(\d+)([smhd])", time_str.lower())
        if not match:
            raise ValueError("Invalid time format. Use something like 10s, 5m, 2h, or 1d.")
        value, unit = match.groups()
        return int(value) * time_units[unit]
    
    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, msgs):
        channel = ctx.channel
        await channel.purge(limit=(int(msgs) + 1))
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} deleted {msgs} messages',colour=0xbc0a1d))


    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=f'{reason} || by: {ctx.author.name}', delete_message_days=0)
        await ctx.send(embed=self.build_embed("Banned", f"{member.display_name} has been banned.\nReason: {reason}", color=0xff0004))
    
    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, identifier: str):
        banned_users = await ctx.guild.bans()
        user = None

        for ban_entry in banned_users:
            if identifier in {str(ban_entry.user.id), str(ban_entry.user), ban_entry.user.name}:
                user = ban_entry.user
                break

        if user is None:
            await ctx.send(embed=self.build_embed("User Not Found", "No matching banned user.", discord.Color.red()))
            return

        await ctx.guild.unban(user)
        await ctx.send(embed=self.build_embed("User Unbanned", f"{user} has been unbanned.", discord.Color.green()))


    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided."):
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=self.build_embed("User Kicked", f"{member.display_name} was kicked.\nReason: {reason}", discord.Color.orange()))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I can't kick this user.", discord.Color.red()))

    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason="No reason provided."):
        try:
            await member.ban(reason=reason, delete_message_days=1)
            await ctx.guild.unban(member)
            await ctx.send(embed=self.build_embed("User Softbanned", f"{member.display_name} was softbanned (messages deleted).\nReason: {reason}", discord.Color.orange()))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I can't softban this user.", discord.Color.red()))


    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided."):
        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        if mutedrole is None:
            mutedrole = discord.utils.get(ctx.guild.roles, name='muted')
        elif mutedrole is None:
            return await ctx.send(embed=discord.Embed(description="Role Muted doesn't exist", colour=0xff0004))
        await member.add_roles(mutedrole, reason = f'{reason} || by {ctx.author.name}')
        if reason == '':
            reason = 'no reason specified'
        await ctx.send(embed=discord.Embed(description=f'{member} muted by: {ctx.author.name} for: {reason}', colour=discord.Color.green))

    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=''):
        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        if mutedrole is None:
            mutedrole = discord.utils.get(ctx.guild.roles, name='muted')
            if mutedrole is None:
                return await ctx.send(embed=discord.Embed(description="Role Muted doesn't exist", colour=0xff0004))
        await member.remove_roles(mutedrole, reason = f'{reason} || by {ctx.author.name}')
        await ctx.send(embed=discord.Embed(description=f'{member} unmuted by {ctx.author.name}', colour=discord.Color.green))
    
    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(manage_roles=True)
    async def tmute(self, ctx, member: discord.Member, duration: str, *, reason="No reason provided."):
        seconds = self.parse_time(duration)
        if seconds is None:
           await ctx.send(embed=self.build_embed("Invalid Duration", "Use `s`, `m`, `h`, or `d` (e.g., `10m`, `2h`)", discord.Color.red()))
           return

        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send(embed=self.build_embed("Missing Role", "Muted role does not exist.", discord.Color.red()))
            return

        try:
            await member.add_roles(muted_role)
            await ctx.send(embed=self.build_embed("User Muted", f"{member.display_name} muted for {duration}.\nReason: {reason}", discord.Color.orange()))

            # Wait, then unmute
            await asyncio.sleep(seconds)
            if muted_role in member.roles:
                await member.remove_roles(muted_role)
                await ctx.send(embed=self.build_embed("Mute Expired", f"{member.display_name} has been automatically unmuted.", discord.Color.green()))

        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I can't modify roles for this user.", discord.Color.red()))



async def setup(bot):
    await bot.add_cog(Moderation(bot))
