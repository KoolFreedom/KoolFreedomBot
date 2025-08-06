import discord
import asyncio
from discord.ext import commands
from util.punishment_manager import get_user_roles

class PunishmentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await asyncio.sleep(2)  # Let other bots finish first
        punishment_roles = get_user_roles(member.guild.id, member.id)

        # Re-assign punishment roles
        roles_to_restore = []
        for role_id in punishment_roles:
            role = member.guild.get_role(role_id)
            if role:
                roles_to_restore.append(role)

        try:
            # Remove all roles except punishment and @everyone
            current_roles = [r for r in member.roles if r != member.guild.default_role]
            for role in current_roles:
                if role not in roles_to_restore:
                    await member.remove_roles(role, reason="Stripping auto-assigned roles")

            # Add back punishment roles (if not already there)
            await member.add_roles(*roles_to_restore, reason="Restoring punishment roles")
        except discord.Forbidden:
            print(f"Missing permissions to manage roles for {member}.")



# In your bot setup:
async def setup(bot):
    await bot.add_cog(PunishmentCog(bot))
