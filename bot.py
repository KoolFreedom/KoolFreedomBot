import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="kf!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(embed=build_embed("Access Denied", "❌ You don't have permission to use this command.", discord.Color.red()))


SERVER_STAFF_ROLES = {"Admin", "Senior Admin", "Executive"}

def has_allowed_role():
    async def predicate(ctx):
        return any(role.name in SERVER_STAFF_ROLES for role in ctx.author.roles)
    return commands.check(predicate)

def build_embed(title, description, color=discord.Color.blue()):
    return discord.Embed(title=title, description=description, color=color)

@bot.command()
@has_allowed_role()
@commands.has_permissions(manage_roles=True)
async def serverban(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name = "Server Banned")
    if role is None:
        await ctx.send(embed=build_embed("Role Not Found", "'Server Banned' role not found!", discord.Color.red()))
        return
    
    try:
        await member.add_roles(role)
        await ctx.send(embed=build_embed("Role Added", f"Added Server Banned role to {member.display_name}.", discord.Color.green()))
    except discord.Forbidden:
        await ctx.send(embed=build_embed("Permission Error", "I don't have permission to assign that role.", discord.Color.red()))
    except Exception as e:
        await ctx.send(embed=build_embed("Error", f"❌ {e}", discord.Color.red()))

@bot.command()
@has_allowed_role()
@commands.has_permissions(manage_roles=True)
async def serverunban(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Server Banned")
    if not role:
        await ctx.send(embed=build_embed("Role Not Found", "'Server Banned' role not found.", discord.Color.red()))
        return

    try:
        await member.remove_roles(role)
        await ctx.send(embed=build_embed("Role Removed", f"Removed Server Banned role from {member.display_name}.", discord.Color.green()))
    except discord.Forbidden:
        await ctx.send(embed=build_embed("Permission Error", "I don't have permission to remove that role.", discord.Color.red()))
    except Exception as e:
        await ctx.send(embed=build_embed("Error", f"❌ {e}", discord.Color.red()))

@bot.command()
@has_allowed_role()
@commands.has_permissions(manage_roles=True)
async def exile(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name = "Exiled")
    member_role = discord.utils.get(ctx.guild.roles, name = "Members")
    if not role:
        await ctx.send(embed=build_embed("Role Not Found", "'Exiled' role not found.", discord.Color.red()))
        return
    try:
        await member.remove_roles(member_role)
        await member.add_roles(role)
        await ctx.send(embed=build_embed("", f"Exiled {member.display_name}.", discord.Color.red()))
    except discord.Forbidden:
        await ctx.send(embed=build_embed("Permission Error", "I don't have permission to assign that role.", discord.Color.red()))
    except Exception as e:
        await ctx.send(embed=build_embed("Error", f"❌ {e}", discord.Color.red()))

@bot.command()
@has_allowed_role()
@commands.has_permissions(manage_roles=True)
async def forgive(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name = "Exiled")
    member_role = discord.utils.get(ctx.guild.roles, name = "Members")
    if not role:
        await ctx.send(embed=build_embed("Role Not Found", "'Exiled' role not found.", discord.Color.red()))
        return
    try:
        await member.add_roles(member_role)
        await member.remove_roles(role)
        await ctx.send(embed=build_embed("", f"Forgave {member.display_name}.", discord.Color.green()))
    except discord.Forbidden:
        await ctx.send(embed=build_embed("Permission Error", "I don't have permission to assign that role.", discord.Color.red()))
    except Exception as e:
        await ctx.send(embed=build_embed("Error", f"❌ {e}", discord.Color.red()))



bot.run("MTA4ODE2OTU1MjYwNjY3OTEyMQ.G-eEn7.OElufEYnwR3ppO41QVwDRWGoxDOTEU3maBmFmE")