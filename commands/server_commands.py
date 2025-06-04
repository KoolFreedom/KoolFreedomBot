import discord
from discord.ext import commands
from checks import is_admin, is_discord_staff


class Server_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def build_embed(self, title, description, color=discord.Color.green()):
        return discord.Embed(title=title, description=description, color=color)
    
    @commands.command()
    @is_admin()
    @commands.has_permissions(manage_roles=True)
    async def serverban(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name = "Server Banned")
        if role is None:
            await ctx.send(embed=self.build_embed("Role Not Found", "'Server Banned' role not found!", discord.Color.red()))
            return
    
        try:
            await member.add_roles(role)
            await ctx.send(embed=self.build_embed("Role Added", f"Added Server Banned role to {member.display_name}.", discord.Color.green()))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I don't have permission to assign that role.", discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", f":x: {e}", discord.Color.red()))

    @commands.command()
    @is_admin()
    @commands.has_permissions(manage_roles=True)
    async def serverunban(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Server Banned")
        if not role:
            await ctx.send(embed=self.build_embed("Role Not Found", "'Server Banned' role not found.", discord.Color.red()))
            return

        try:
            await member.remove_roles(role)
            await ctx.send(embed=self.build_embed("Role Removed", f"Removed Server Banned role from {member.display_name}.", discord.Color.green()))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I don't have permission to remove that role.", discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", f":x: {e}", discord.Color.red()))

    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(manage_roles=True)
    async def exile(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name = "Exiled")
        member_role = discord.utils.get(ctx.guild.roles, name = "Members")
        if not role:
            await ctx.send(embed=self.build_embed("Role Not Found", "'Exiled' role not found.", discord.Color.red()))
            return
        try:
            await member.remove_roles(member_role)
            await member.add_roles(role)
            await ctx.send(embed=self.build_embed("", f"Exiled {member.display_name}.", discord.Color.red()))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I don't have permission to assign that role.", discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", f":x: {e}", discord.Color.red()))

    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(manage_roles=True)
    async def forgive(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name = "Exiled")
        member_role = discord.utils.get(ctx.guild.roles, name = "Members")
        if not role:
            await ctx.send(embed=self.build_embed("Role Not Found", "'Exiled' role not found.", discord.Color.red()))
            return
        try:
            await member.add_roles(member_role)
            await member.remove_roles(role)
            await ctx.send(embed=self.build_embed("", f"Forgave {member.display_name}.", discord.Color.green()))
        except discord.Forbidden:
            await ctx.send(embed=self.build_embed("Permission Error", "I don't have permission to assign that role.", discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", f":x: {e}", discord.Color.red()))

async def setup(bot):
    await bot.add_cog(Server_Commands(bot))