import discord
from discord.ext import commands
import pytz
import json
from datetime import datetime
from pathlib import Path

TIMEZONE_FILE = Path("data/timezones.json")
TIMEZONE_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load or initialize timezone data
if TIMEZONE_FILE.exists():
    with open(TIMEZONE_FILE, 'r') as f:
        timezone_data = json.load(f)
else:
    timezone_data = {}

class Timezone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def save_timezones(self):
        with open(TIMEZONE_FILE, 'w') as f:
            json.dump(timezone_data, f, indent=2)

    @commands.command()
    async def settimezone(self, ctx, timezone: str):
        if timezone not in pytz.all_timezones:
            await ctx.send("❌ Invalid timezone. Try one from: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
            return

        timezone_data[str(ctx.author.id)] = timezone
        self.save_timezones()
        await ctx.send(f"✅ Timezone set to `{timezone}`.")

    @commands.command()
    async def timefor(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        tz = timezone_data.get(str(member.id))

        if not tz:
            await ctx.send("⚠️ That user hasn't set a timezone yet.")
            return

        now = datetime.now(pytz.timezone(tz))
        await ctx.send(f"🕒 Current time for **{member.display_name}**: `{now.strftime('%Y-%m-%d %H:%M:%S')}` ({tz})")

    @commands.command()
    async def convert(self, ctx, time: str, from_tz: str, to_tz: str):
        if from_tz not in pytz.all_timezones or to_tz not in pytz.all_timezones:
            await ctx.send("❌ Invalid timezone(s). Check spelling from the timezone list.")
            return

        try:
            naive_time = datetime.strptime(time, "%H:%M")
            from_zone = pytz.timezone(from_tz)
            to_zone = pytz.timezone(to_tz)

            from_dt = from_zone.localize(naive_time)
            to_dt = from_dt.astimezone(to_zone)

            await ctx.send(f"🕓 `{time}` in `{from_tz}` is `{to_dt.strftime('%H:%M')}` in `{to_tz}`.")
        except Exception as e:
            await ctx.send(f"❌ Error parsing time. Use `HH:MM` 24h format. {e}")

async def setup(bot):
    await bot.add_cog(Timezone(bot))
