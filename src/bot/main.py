import asyncio
import pathlib

import colorama
import discord
from discord.ext import commands

from bot.modules import database
from bot.utils import get_discord_token


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")


async def load_cogs():
    cogs_path = pathlib.Path(__file__).parent / "cogs"

    for file in sorted(cogs_path.glob("*.py")):
        if file.name.startswith("_"):
            continue
        ext = f"bot.cogs.{file.stem}"

        try:
            await bot.load_extension(ext)
            print(f"{colorama.Fore.GREEN}[✓]{colorama.Fore.RESET} Extension {ext} loaded successfully")
        except Exception as e:
            print(f"{colorama.Fore.RED}[x]{colorama.Fore.RESET} Extension {ext} failed to load. Details below:\n{e}")
        
async def async_main():
    token = ""
    try:
        token = get_discord_token()
    except Exception as e:
        print(f"{colorama.Fore.RED}[x]{colorama.Fore.RESET} {e}")
        exit(1)

    database.init_db()
    await load_cogs()
    await bot.start(token)

def main():
    asyncio.run(async_main())