import colorama
import sqlmodel

from bot.modules.models import User
from bot.utils import get_database_url


_engine = None

def get_engine():
    global _engine

    url = ""
    try:
        url = get_database_url()
    except Exception as e:
        print(f"{colorama.Fore.RED}[x]{colorama.Fore.RESET} {e}")
        exit(1)

    if _engine is None:
        _engine = sqlmodel.create_engine(url, echo=False)
    
    return _engine

def get_session():
    return sqlmodel.Session(get_engine())

def init_db():
    sqlmodel.SQLModel.metadata.create_all(get_engine())
