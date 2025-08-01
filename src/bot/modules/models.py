from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    guild_id: int = Field()
    message_count: int = Field(default=0)
    