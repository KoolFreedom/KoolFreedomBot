import discord
import asyncio
import re
from discord.ext import commands
from checks import is_discord_staff

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, title, description, color=discord.Color.blue()):
        return discord.Embed(title=title, description=description, color=color)
    
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
    async def purge(self, ctx: commands.Context, amount: int):
        deleted = await ctx.channel.purge(limit=amount + 1)
        count = len(deleted) - 1  # Subtract 1 for the command message itself
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} deleted {count} messages',colour=0xbc0a1d), delete_after=5)


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
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send(embed=self.build_embed("Missing Role", "Muted role does not exist", discord.Color.red))
            return
        try:
            await member.add_roles(muted_role)
            await ctx.send(embed=self.build_embed("Muted", f"{member.display_name} has been muted.\nReason: {reason}", discord.Color.green))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permissions Error", "I do not have permission to do this", discord.Color.red))

    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send(embed=self.build_embed("Missing Role", "Muted role does not exist.", discord.Color.red()))
            return

        try:
            await member.remove_roles(muted_role)
            await ctx.send(embed=self.build_embed("User Unmuted", f"{member.display_name} has been unmuted.", discord.Color.green()))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I don't have permission to remove roles.", discord.Color.red()))
    
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
