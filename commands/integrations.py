import discord
from discord.ext import commands
import aiohttp
import random

class Integrations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, title, description, color=discord.Color.blue()):
        return discord.Embed(title=title, description=description, color=color)

    @commands.command()
    async def weather(self, ctx, *, location: str):
        url = f"https://wttr.in/{location}?format=3"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.text()
                        await ctx.send(embed=self.build_embed("Weather", data, discord.Color.blue()))
                    else:
                        await ctx.send(embed=self.build_embed("Error", "Could not fetch weather.", discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Exception", str(e), discord.Color.red()))

    @commands.command(aliases=["mc"])
    async def mcstatus(self, ctx, ip: str):
        url = f"https://api.mcsrvstat.us/2/{ip}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await ctx.send(embed=self.build_embed("Error", "Could not reach API.", discord.Color.red()))
                        return

                    data = await resp.json()
                    if not data.get("online"):
                        await ctx.send(embed=self.build_embed("Offline", f"The server `{ip}` is offline.", discord.Color.red()))
                        return

                    description = "\n".join(data["motd"]["clean"]) if data.get("motd") else "No MOTD"
                    embed = discord.Embed(
                        title=f"Status for {ip}",
                        description=description,
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Players", value=f"{data['players']['online']}/{data['players']['max']}", inline=True)
                    embed.add_field(name="Version", value=data.get("version", "Unknown"), inline=True)
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", str(e), discord.Color.red()))

    @commands.command()
    async def paste(self, ctx, *, content: str):
        url = "https://hastebin.com/documents"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=content.encode()) as resp:
                    if resp.status != 200:
                        await ctx.send(embed=self.build_embed("Error", "Failed to upload to Hastebin.", discord.Color.red()))
                        return
                    data = await resp.json()
                    paste_url = f"https://hastebin.com/{data['key']}"
                    await ctx.send(embed=self.build_embed("Paste Created", paste_url, discord.Color.blue()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", str(e), discord.Color.red()))

    @commands.command()
    async def github(self, ctx, repo: str):
        url = f"https://api.github.com/repos/{repo}/events"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status != 200:
                        await ctx.send(embed=self.build_embed("Error", f"Could not fetch data for `{repo}`.", discord.Color.red()))
                        return

                    data = await resp.json()
                    if not data:
                        await ctx.send(embed=self.build_embed("No Activity", "No recent activity found.", discord.Color.orange()))
                        return

                    latest = data[0]
                    event_type = latest.get("type", "Unknown Event")
                    actor = latest["actor"]["login"]
                    action = f"{actor} triggered a **{event_type}** event"

                    embed = discord.Embed(
                        title=f"{repo}",
                        description=action,
                        url=f"https://github.com/{repo}",
                        color=discord.Color.blurple()
                    )
                    embed.set_footer(text="Latest GitHub event")
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", str(e), discord.Color.red()))

    @commands.command()
    async def fact(self, ctx):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    fact = data.get("text", "Couldn't fetch a fact.")
                    await ctx.send(embed=self.build_embed("Random Fact", fact, discord.Color.purple()))
        except Exception as e:
            await ctx.send(embed=self.build_embed("Error", str(e), discord.Color.red()))

    @commands.command(name="nowplaying", aliases=["np"])
    async def now_playing(self, ctx):
        activity = ctx.bot.user.activity
        if not activity:
            await ctx.send(embed=self.build_embed("Now Playing", "I'm not doing anything right now.", discord.Color.greyple()))
        else:
            name = activity.name or "Unnamed"
            kind = type(activity).__name__.replace("Activity", "")
            await ctx.send(embed=self.build_embed("Now Playing", f"{kind}: {name}", discord.Color.teal()))

async def setup(bot):
    await bot.add_cog(Integrations(bot))
