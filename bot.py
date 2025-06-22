import discord
from discord.ext import commands
import os
import json
import asyncio

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(message.guild.id), getattr(bot, "default_prefix", "!"))

def build_embed(title, description, color=discord.Color.green()):
        return discord.Embed(title=title, description=description, color=color)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.default_prefix = "kf!"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(embed=build_embed("Access Denied", "❌ You don't have permission to use this command.", discord.Color.red()))

async def load_cogs():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start("TOKEN")

# Start the bot
asyncio.run(main())
