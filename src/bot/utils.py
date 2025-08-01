import os

import dotenv


dotenv.load_dotenv()

def get_discord_token() -> str:
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env")
    return token

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")

    if not url:
        raise RuntimeError("DATABASE_URL not set in .env")
    return url