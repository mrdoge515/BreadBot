import datetime

import colorama
from discord.ext import tasks, commands
from sqlmodel import select, delete

from bot.modules import database
from bot.modules.models import Reminder, User_Timezone


class Reminder_Task(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_db_and_remind.start()

    async def cog_unload(self):
        self.check_db_and_remind.cancel()

    async def remind(self, user_id: int, text: str):
        try:
            user = await self.bot.fetch_user(user_id)

            if user:
                await user.send(f"🔔 ┃ {text}")
        except Exception as e:
            print(f"{colorama.Fore.RED}[x]{colorama.Fore.RESET} Failed to send a reminder to {user_id}: {e}")
    
    @tasks.loop(minutes=1)
    async def check_db_and_remind(self):
        now = datetime.datetime.now(datetime.timezone.utc)

        with database.get_session() as session:
            statement = select(Reminder).where(Reminder.time <= now)
            results = session.exec(statement).all()

            for reminder in results:
                await self.remind(reminder.user_id, reminder.text)

                statement = delete(Reminder).where(Reminder.id == reminder.id)
                session.exec(statement)
            
            session.commit()


async def setup(bot: commands.Bot):
    await bot.add_cog(Reminder_Task(bot))
