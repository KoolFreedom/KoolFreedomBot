import discord
import time
import json
from checks import is_discord_staff
from datetime import datetime
from discord.ext import commands


start_time = time.time()

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, title, description, color=discord.Color.green()):
        return discord.Embed(title=title, description=description, color=color)

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(embed=self.build_embed("Pong! 🏓", f"Latency: {latency}ms"))

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"User Info - {member.display_name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime('%Y-%m-%d'), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def uptime(self, ctx):
        uptime_seconds = int(time.time() - start_time)
        uptime_string = str(datetime.utcfromtimestamp(uptime_seconds).strftime("%H:%M:%S"))
        await ctx.send(embed=self.build_embed("Bot Uptime", uptime_string, discord.Color.blurple()))

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(embed=self.build_embed("Prefix Changed", f"New prefix is now `{new_prefix}`", discord.Color.blue()))


async def setup(bot):
    await bot.add_cog(Utility(bot))
