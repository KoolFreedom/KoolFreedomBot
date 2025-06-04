# checks.py

from discord.ext import commands

SERVER_STAFF_ROLES = ["Moderator", "Admin", "Senior Admin"]
DISCORD_STAFF_ROLES = ["Discord Mod", "Discord Admin"]
BOT_DEVELOPERS = [373969695633571842, 712528833936621730, 919085826875469834]

def has_allowed_role():
    async def predicate(ctx):
        return any(role.name in SERVER_STAFF_ROLES for role in ctx.author.roles)
    return commands.check(predicate)

def is_discord_staff():
    async def predicate(ctx):
        return any(role.name in DISCORD_STAFF_ROLES for role in ctx.author.roles)
    return commands.check(predicate)

def is_bot_dev():
    async def predicate(ctx):
        user_id = ctx.author.id
        user_tag = f"{ctx.author.name}#{ctx.author.discriminator}"
        return user_id in BOT_DEVELOPERS or user_tag in BOT_DEVELOPERS
    return commands.check(predicate)
