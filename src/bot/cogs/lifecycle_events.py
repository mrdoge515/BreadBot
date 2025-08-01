import colorama
import discord
from discord.ext import commands


class Lifecycle_Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        activity = discord.Activity(type=discord.ActivityType.watching, name="the oven")
        await self.bot.change_presence(activity=activity)
        print(f"{colorama.Fore.GREEN}[✓]{colorama.Fore.RESET} {self.bot.user} just went online!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Lifecycle_Events(bot)) 