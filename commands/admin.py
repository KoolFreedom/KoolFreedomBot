import discord
import os
import sys
import subprocess
from discord.ext import commands
from checks import is_discord_staff, is_bot_dev

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, title, description, color=discord.Color.green()):
        return discord.Embed(title=title, description=description, color=color)

    @commands.command()
    @is_discord_staff()
    async def lockdown(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=self.build_embed("Channel Locked", "Users can no longer send messages here.", discord.Color.red()))

    @commands.command()
    @is_discord_staff()
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=self.build_embed("Channel Unlocked", "Users can send messages again.", discord.Color.green()))

    @commands.command()
    @is_bot_dev()
    async def stop(self, ctx):
        await ctx.send(embed=self.build_embed(f"Shutting down...", color=0xff0000))
        await self.bot.close()

    @commands.command()
    @is_bot_dev()
    async def restart(self, ctx):
        await ctx.send(embed=self.build_embed(f"Restarting...", color=0xff0000))
        await self.bot.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    @commands.command()
    @is_bot_dev()
    async def reload(self, ctx, cog: str):
        try:
            await self.bot.reload_extension(f"commands.{cog}")
            await ctx.send(embed=self.build_embed("Reloaded", f"Successfully reloaded `{cog}`", discord.Color.green()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", f"Failed to reload `{cog}`\n```{e}```", discord.Color.red()))

    @commands.command(aliases=["updatebot", "pull"])
    @is_bot_dev()
    async def gitpull(self, ctx):
        try:
            result = subprocess.run(
                ["git", "pull"],
                capture_output=True,
                text=True
            )
            output = result.stdout or result.stderr
            color = discord.Color.green() if result.returncode == 0 else discord.Color.red()

            embed = discord.Embed(
                title="🔄 Git Pull Result",
                description=f"```{output.strip()}```",
                color=color
            )
            await ctx.send(embed=embed)

            if result.returncode != 0:
                return  # Don't restart if pull failed

            await ctx.send("♻️ Update complete. Restarting bot...")

            # Optional: give Discord time to receive the message
            await self.bot.close()  # Clean disconnect from Discord

            # Restart process
            os.execv(sys.executable, [sys.executable] + sys.argv)

        except Exception as e:
            await ctx.send(f"❌ Error during git pull or restart:\n```{e}```")

async def setup(bot):
    await bot.add_cog(Admin(bot))