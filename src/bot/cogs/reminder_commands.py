from zoneinfo import ZoneInfo

import discord
import sqlmodel
from discord.ext import commands

from bot.modules import database
from bot.modules.models import User_Timezone


class Reminder_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @discord.app_commands.command(
            name="settimezone",
            description="Set your timezone (used for the reminder command)"
    )
    @discord.app_commands.describe(tz="IANA timezone name, e.g., America/New_York, Europe/Warsaw")
    async def settimezone(self, interaction: discord.Interaction, tz: str):
        try:
            _ = ZoneInfo(tz)
        except Exception:
            await interaction.response.send_message("❌ Invalid timezone. Use an IANA name.", ephemeral=True)
            return
        
        with database.get_session() as session:
            statement = (
                sqlmodel.delete(User_Timezone)
                .where(User_Timezone.user_id == interaction.user.id)
            )
            session.exec(statement)
            
            statement = (
                sqlmodel.insert(User_Timezone)
                .values(user_id = interaction.user.id, timezone = tz)
            )
            session.exec(statement)

            session.commit()
        
        await interaction.response.send_message(
            f"✔️ Timezone set to `{tz}`. Future reminders will be interpreted in that zone.",
            ephemeral=True
        )


    remind = discord.app_commands.Group(name="remind", description="BreadBot will send you a reminder!")

    @remind.command(
        name="on",
        description="Remind at an absolute time. Example: 11-09-2001 14:46"
    )
    @discord.app_commands.describe(
        when="Absolute datetime in format: DD-MM-YYYY HH:MM",
        text="What you want to be reminded about"
    )
    async def on(self, interaction: discord.Interaction, when: str, text: str):
        await interaction.response.send_message("Work in progress", ephemeral=True)

    @remind.command(
        name="in",
        description="Remind in specified time. Example 3h"
    )
    @discord.app_commands.describe(
        offset="Relative time like 2m, 13h, 7d",
        text="What you want to be reminded about"
    )
    async def in_(self, interaction: discord.Interaction, offset: str, text: str):
        await interaction.response.send_message("Work in progress", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Reminder_Commands(bot))