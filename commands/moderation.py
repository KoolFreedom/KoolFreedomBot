import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, title, description, color=discord.Color.blue()):
        return discord.Embed(title=title, description=description, color=color)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(embed=self.build_embed("Banned", f"{member.display_name} has been banned.\nReason: {reason}"))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role:
            await member.add_roles(role)
            await ctx.send(embed=self.build_embed("Muted", f"{member.display_name} has been muted."))
        else:
            await ctx.send(embed=self.build_embed("Error", "Muted role not found.", discord.Color.red()))

async def setup(bot):
    await bot.add_cog(Moderation(bot))
