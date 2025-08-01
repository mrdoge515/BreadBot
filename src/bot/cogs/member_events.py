import discord
from discord.ext import commands
from sqlmodel import delete

from bot.modules import database
from bot.modules.models import User


class Member_Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with database.get_session() as session:
            user = User(user_id=member.id, guild_id=member.guild.id)
            session.add(user)
            session.commit()

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        with database.get_session() as session:
            statement = delete(User).where((User.guild_id == member.guild.id) & (User.user_id == member.id))
            session.exec(statement=statement)
            session.commit()

async def setup(bot: commands.Bot):
    await bot.add_cog(Member_Events(bot)) 