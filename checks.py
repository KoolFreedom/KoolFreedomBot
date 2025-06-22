from discord.ext import commands

ADMIN_ROLES = ["Admin", "CONSOLE"]
SENIOR_ROLES = ["Senior Admin", "Executive", "Assistant Executive"]
DISCORD_STAFF_ROLES = ["Discord Moderator", "Discord Administrator"]
ADMIN_OFFICER = ["Admin Officer"]
MB_MANAGER = ["MB Manager"]
BOT_DEVELOPERS = [373969695633571842, 712528833936621730, 919085826875469834]

def is_admin():
    async def predicate(ctx):
        return any(role.name in ADMIN_ROLES for role in ctx.author.roles)
    return commands.check(predicate)

def is_senior_admin():
    async def predicate(ctx):
        return any(role.name in SENIOR_ROLES for role in ctx.author.roles)
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

def is_admin_officer():
    async def predicate(ctx):
        return any(role.name in ADMIN_OFFICER for role in ctx.author.roles)
    return commands.check(predicate)

def is_builder_manager():
    async def predicate(ctx):
        return any(role.name in MB_MANAGER for role in ctx.author.roles)
    return commands.check(predicate)