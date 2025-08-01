from sqlalchemy import BigInteger
from sqlmodel import SQLModel, Column, Field


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(sa_column=Column(BigInteger))
    guild_id: int = Field(sa_column=Column(BigInteger))
    message_count: int = Field(default=0)
    