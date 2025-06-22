import discord
import time
import json
import psutil
import platform
import pyfiglet
import random
from checks import is_discord_staff
from datetime import datetime, timedelta
from discord.ext import commands


start_time = time.time()

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, title, description, color=discord.Color.green()):
        return discord.Embed(title=title, description=description, color=color)

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(embed=self.build_embed("Pong! 🏓", f"Latency: {latency}ms"))

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member=None):
        if not user: user=ctx.author
        msg = discord.Embed(title=f'User Information: {user}', color=0xbc0a1d)
        msg.set_thumbnail(url=user.avatar_url)
        msg.add_field(name='Username', value = f'{user.name}')
        msg.add_field(name='Nick', value = f'{user.nick}')
        msg.add_field(name='ID', value = f'{user.id}')
        msg.add_field(name='Avatar URL', value = f'{user.avatar_url}')
        msg.add_field(name='Status', value = f'{user.status}')
        msg.add_field(name='Activity', value = f'{user.activity}')
        msg.add_field(name='Bot?', value = f'{user.bot}')
        msg.add_field(name='Account Creation Date', value = f'{user.created_at}')
        msg.add_field(name='Guild Join Date', value = f'{user.joined_at}')
        msg.add_field(name='On a Phone?', value = f'{user.is_on_mobile()}')
        await ctx.send(embed=msg)
    
    @commands.command()
    async def uptime(self, ctx):
        uptime_seconds = int(time.time() - start_time)
        uptime_string = str(datetime.utcfromtimestamp(uptime_seconds).strftime("%H:%M:%S"))
        await ctx.send(embed=self.build_embed("Bot Uptime", uptime_string, discord.Color.blurple()))

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        msg = discord.Embed(title='Server Information', color=0xbc0a1d)
        msg.set_thumbnail(url=guild.icon_url_as(format='png'))
        msg.add_field(name='Name', value = f'{guild.name}')
        msg.add_field(name='ID', value = f'{guild.id}')
        msg.add_field(name='Description', value = f'{guild.description}')
        msg.add_field(name='Region', value = f'{guild.region}')
        msg.add_field(name='Owner', value = f'{guild.owner}')
        msg.add_field(name='Members', value = f'{guild.member_count}')
        msg.add_field(name='Guild Creation Date', value = f'{guild.created_at}')
        msg.add_field(name='Role Count', value = f'{len(guild.roles)}')
        msg.add_field(name=f'Channel Count ({len(guild.channels)} Total)', value = f'{len(guild.voice_channels)} voice, {len(guild.text_channels)} text')
        msg.add_field(name='Boost Level', value = f'{guild.premium_tier}')
        msg.add_field(name='AFK Timeout', value = f'{guild.afk_timeout/60} minutes')
        msg.add_field(name='AFK Channel', value = f'{guild.afk_channel}')
        await ctx.send(embed=msg)
    
    @commands.command()
    @is_discord_staff()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(embed=self.build_embed("Prefix Changed", f"New prefix is now `{new_prefix}`", discord.Color.blue()))

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(embed=self.build_embed(
            f"{member.display_name}'s Avatar",
            f"[Click here]({member.display_avatar.url})",
            discord.Color.purple()
    )   .set_image(url=member.display_avatar.url))
        
    @commands.command()
    async def roleinfo(self, ctx, *, role: discord.Role):
        embed = discord.Embed(title=f"Role Info - {role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Members", value=len(role.members))
        embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Mentionable", value=role.mentionable)
        await ctx.send(embed=embed)


    @commands.command()
    async def botinfo(self, ctx):
        bot = self.bot
        proc = psutil.Process()
        with proc.oneshot():
            uptime = timedelta(seconds=int(time.time() - start_time))
            cpu_usage = proc.cpu_percent() / psutil.cpu_count()
            mem = proc.memory_full_info()
            memory_usage = mem.rss / 1024**2

        embed = discord.Embed(title="🤖 Bot Information", color=discord.Color.blurple())
        embed.add_field(name="Bot Name", value=bot.user.name, inline=True)
        embed.add_field(name="Bot ID", value=bot.user.id, inline=True)
        embed.add_field(name="Owner", value="<@373969695633571842>", inline=True)
        embed.add_field(name="Uptime", value=str(uptime), inline=True)
        embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
        embed.add_field(name="Users", value=sum(g.member_count for g in bot.guilds), inline=True)
        embed.add_field(name="Commands", value=len(bot.commands), inline=True)
        embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Memory Usage", value=f"{memory_usage:.2f} MB", inline=True)
        embed.add_field(name="CPU Usage", value=f"{cpu_usage:.2f}%", inline=True)

        # Add loaded cogs list
        loaded_cogs = list(bot.cogs.keys())
        if loaded_cogs:
            formatted_cogs = ", ".join(cog.title() for cog in loaded_cogs[:10])
            if len(loaded_cogs) > 10:
                formatted_cogs += f" ...and {len(loaded_cogs) - 10} more"
            embed.add_field(name="Loaded Cogs", value=formatted_cogs, inline=False)
        else:
            embed.add_field(name="Loaded Cogs", value="No cogs loaded.", inline=False)

        embed.set_footer(text=f"Python {platform.python_version()} | discord.py {discord.__version__}")
        embed.set_thumbnail(url=bot.user.display_avatar.url)

        await ctx.send(embed=embed)


    @commands.command()
    async def say(self, ctx, *, msg):
        cmdmsg = ctx.message
        #if '@everyone' in cmdmsg.content or '@here' in cmdmsg.content:
            #msg.replace('@everyone', '[MENTIONED EVERYONE]')
        if cmdmsg.role_mentions:
            index = msg.find('@')
            msg = msg[:index] + '\\'+ msg[index:]
        await ctx.send(f'{msg}')
        try:
            await cmdmsg.delete()
        except:
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Say] Failed to delete a message.")

    @commands.command()
    async def ascii(self, ctx, *, text: str):
        if len(text) > 20:
            return await ctx.send("❌ Text too long. Please limit to 20 characters.")
        ascii_text = pyfiglet.figlet_format(text)
        await ctx.send(f"```{ascii_text}```")

    @commands.command(name="8ball", aliases=["eightball"])
    async def eightball(self, ctx, *, question: str):
        responses = [
            "Yes.", "No.", "Maybe.", "Definitely.", "Absolutely not.",
            "Ask again later.", "Without a doubt.", "Very doubtful.",
            "I'm not sure.", "It is certain."
        ]
        response = random.choice(responses)
        await ctx.send(embed=self.build_embed("🎱 8ball", f"**Question:** {question}\n**Answer:** {response}"))
    
    
async def setup(bot):
    await bot.add_cog(Utility(bot))
