import discord
from discord.ext import commands
from sqlmodel import delete

from bot.modules import database
from bot.modules.models import User


class Guild_Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        members: list[discord.Member] = [member async for member in guild.fetch_members()]

        with database.get_session() as session:
            for member in members:
                if member.id != self.bot.user.id:
                    user = User(user_id=member.id, guild_id=member.guild.id)
                    session.add(user)
            
            session.commit()
                    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        with database.get_session() as session:
            statement = delete(User).where(User.guild_id == guild.id)
            session.exec(statement=statement)
            session.commit()

async def setup(bot: commands.Bot):
    await bot.add_cog(Guild_Events(bot)) 