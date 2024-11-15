from sqlalchemy import BigInteger, ForeignKey, String, Double, Date, Nullable, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import List
from datetime import date

from config import ENGINE, ECHO

engine = create_async_engine(url=ENGINE, echo = ECHO)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass
'''
botTelegramUser(id, tgId, username, verificationCode, endTimeVerificationCode)
botMinecraftUser(id, name, uid, botTelegramUser_id)
'''


class user(Base):
    __tablename__ = 'botTelegramUser'

    id: Mapped[int] = mapped_column(primary_key=True)
    tgId: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[String] = mapped_column(String, nullable=True)
    verificationCode: Mapped[String] = mapped_column(String, nullable=True)
    endTimeVerificationCode: Mapped[String] = mapped_column(String, nullable=True)
    reward: Mapped[Boolean] = mapped_column(Boolean, default=False)
    notBanned: Mapped[Boolean] = mapped_column(Boolean, default=True)

    bot_rel: Mapped[List['userMinecraft']] = relationship(back_populates='user_rel')
    support_rel: Mapped[List['support']] = relationship(back_populates='user_rel')

class userMinecraft(Base):
    __tablename__ = 'botMinecraftUser'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String)
    botTelegramUser_id: Mapped[int] = mapped_column(ForeignKey('botTelegramUser.id'))

    user_rel: Mapped['user'] = relationship(back_populates='bot_rel')

class support(Base):
    __tablename__ = 'support'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String)
    check: Mapped[Boolean] = mapped_column(Boolean, default=False)
    botTelegramUser_id: Mapped[int] = mapped_column(ForeignKey('botTelegramUser.id'))

    user_rel: Mapped['user'] = relationship(back_populates='support_rel')

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)