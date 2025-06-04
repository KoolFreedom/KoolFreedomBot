import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="kf!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def build_embed(title, description, color=discord.Color.blue()):
    return discord.Embed(title=title, description=description, color=color)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def serverban(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name = "Server Banned")
    if role is None:
        await ctx.send(embed=build_embed("Role Not Found", "'Server Banned' role not found!", discord.Color.red()))
        return
    
    try:
        await member.add_roles(role)
        await ctx.send(embed=build_embed("Role Added", f"Added Server Banned role to {member.display_name}."))
    except discord.Forbidden:
        await ctx.send(embed=build_embed("Permission Error", "I don't have permission to assign that role.", discord.Color.red()))
    except Exception as e:
        await ctx.send(embed=build_embed("Error", f"❌ {e}", discord.Color.red()))

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removevip(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Server Banned")
    if not role:
        await ctx.send(embed=build_embed("Role Not Found", "'Server Banned' role not found.", discord.Color.red()))
        return

    try:
        await member.remove_roles(role)
        await ctx.send(embed=build_embed("Role Removed", f"Removed Server Banned role from {member.display_name}."))
    except discord.Forbidden:
        await ctx.send(embed=build_embed("Permission Error", "I don't have permission to remove that role.", discord.Color.red()))
    except Exception as e:
        await ctx.send(embed=build_embed("Error", f"❌ {e}", discord.Color.red()))




bot.run("MTA0MjExOTI4MDg1MTk2MzkxNA.GMGzio.qGoTh0aSoj-jBMKSQ48kPdj16ORghoEaerxapE")