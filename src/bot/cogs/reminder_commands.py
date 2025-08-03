import datetime
import re
from zoneinfo import ZoneInfo

import discord
import sqlmodel
from discord.ext import commands

from bot.modules import database
from bot.modules.models import Reminder, User_Timezone


def get_user_tz(user_id: int) -> ZoneInfo:
    with database.get_session() as session:
        statement = (
            sqlmodel.select(User_Timezone.timezone)
            .where(User_Timezone.user_id == user_id)
            .limit(1)
        )
        result = session.exec(statement).one_or_none()
        session.commit()

    tz = result if result else "UTC"
    try:
        return ZoneInfo(tz)
    except Exception:
        return ZoneInfo("UTC")
    

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
        source_tz = get_user_tz(interaction.user.id)
        
        try:
            user_time = datetime.datetime.strptime(when, "%d-%m-%Y %H:%M")
            user_time = user_time.replace(tzinfo=source_tz)
            target_utc = user_time.astimezone(datetime.timezone.utc)
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid format! Use `DD-MM-YYYY HH:MM`, e.g. `30-09-2025 14:30`.",
                ephemeral=True
            )
            return
        
        with database.get_session() as session:
            reminder = Reminder(user_id=interaction.user.id, time=target_utc, text=text)
            session.add(reminder)
            session.commit()

        target_in_user = target_utc.astimezone(tz=source_tz)
        fmt = target_in_user.strftime("%Y-%m-%d %H:%M %Z")
        await interaction.response.send_message(
            f"🕒 Absolute reminder set for **{fmt}** — Text: {text}",
            ephemeral=True
        )

    @remind.command(
        name="in",
        description="Remind in specified time. Example 3h"
    )
    @discord.app_commands.describe(
        offset="Relative time like 2m, 13h, 7d",
        text="What you want to be reminded about"
    )
    async def in_(self, interaction: discord.Interaction, offset: str, text: str):
        match = re.fullmatch(r"(\d+)([smhdw])", offset.strip().lower())
        if not match:
            await interaction.response.send_message(
                "❌ Invalid format. Use formats like `15m`, `3h`, `2d`, `1w`",
                ephemeral=True)
            return
        
        amount, unit = match.groups()
        amount = int(amount)

        multipliers = {
            "s": {"seconds": amount},
            "m": {"minutes": amount},
            "h": {"hours": amount},
            "d": {"days": amount},
            "w": {"weeks": amount},
        }

        delta = datetime.timedelta(**multipliers[unit])
        target = datetime.datetime.now(datetime.timezone.utc) + delta

        with database.get_session() as session:
            reminder = Reminder(user_id=interaction.user.id, time=target, text=text)
            session.add(reminder)
            session.commit()
        
        await interaction.response.send_message(
            f"🕒 Parsed relative reminder: {target.isoformat()} (UTC)\nText: {text}",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Reminder_Commands(bot))