import discord
from discord.ext import commands
from sqlmodel import update

from bot.modules import database
from bot.modules.models import User


def remove_skin_tones(text: str) -> str:
    SKIN_TONES = {
        "\U0001F3FB",  # light skin tone
        "\U0001F3FC",  # medium-light skin tone
        "\U0001F3FD",  # medium skin tone
        "\U0001F3FE",  # medium-dark skin tone
        "\U0001F3FF",  # dark skin tone
    }
    return ''.join(ch for ch in text if ch not in SKIN_TONES)

class Message_Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return

        content = remove_skin_tones(message.content.strip()).lower()
        if "Bread 👍" in content:
            await message.reply("Bread 👍")
    
        with database.get_session() as session:
            statement = (
                update(User)
                .where((User.guild_id == message.guild.id) & (User.user_id == message.author.id))
                .values(message_count=User.message_count + 1)
            )
            session.exec(statement=statement)
            session.commit()


    
async def setup(bot: commands.Bot):
    await bot.add_cog(Message_Events(bot)) 