import discord
import os
import sys
from discord.ext import commands
from checks import is_bot_dev

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
    @is_bot_dev()
    async def stop(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.close()

    @commands.command()
    @is_bot_dev()
    async def restart(self, ctx):
        await ctx.send("Restarting...")
        await self.bot.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)

async def setup(bot):
    await bot.add_cog(Utility(bot))
