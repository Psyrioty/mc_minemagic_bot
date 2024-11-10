from app.database.models import user, userMinecraft
from app.database.models import async_session
import datetime
from datetime import timedelta
import random

from sqlalchemy import select, update, delete


async def setTelegramUser(tgId, username):
    async with async_session() as session:
        _user = await session.scalar(select(user).where(user.tgId == tgId))

        if not _user:
            session.add(user(tgId=tgId, username=username))
            await session.commit()

async def setVerificationCode(tgId):
    randomVerificationCode = [random.choice('QWERTYUIPASDFGHJKLZXCVBNM123456789') for _ in range(10)]
    verificationCode = "".join(randomVerificationCode)
    codeEndDate = datetime.datetime.now() + timedelta(minutes=5)
    async with async_session() as session:
        _user = await session.scalar(select(user).where(user.tgId == tgId))
        await session.execute(update(user).values(verificationCode = verificationCode, endTimeVerificationCode = codeEndDate).where(user.id == _user.id))
        await session.commit()

    return(verificationCode)