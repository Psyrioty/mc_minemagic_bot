from app.database.models import user, userMinecraft, support
from app.database.models import async_session
from app.commands import commands
from app.rconConnector import command
from app.tgBot import bot
import datetime
from datetime import timedelta
from config import ADMIN_ID
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
    codeEndDate = codeEndDate.strftime('%a %b %d %H:%M:%S %Y')
    async with async_session() as session:
        _user = await session.scalar(select(user).where(user.tgId == tgId))
        await session.execute(update(user).values(verificationCode = verificationCode, endTimeVerificationCode = str(codeEndDate)).where(user.id == _user.id))
        await session.commit()

    return(verificationCode)

async def checkVerificationCode(tgId, code, name):
    result = "Аккаунт успешно привязан!"
    try:
        async with async_session() as session:
            _user = await session.scalar(select(user).where(user.tgId == tgId))
            endCodeTime = datetime.datetime.strptime(_user.endTimeVerificationCode, '%a %b %d %H:%M:%S %Y')

            if (code == _user.verificationCode and datetime.datetime.now() <= endCodeTime):
                try:
                    session.add(userMinecraft(name=name, botTelegramUser_id=_user.id))
                    await session.commit()
                except:
                    result = "Не удалось привязать аккаунт!"
            else:
                result = "Не верный код или превышено время авторизации!"
    except:
        result = "Не удалось привязать аккаунт!"
    return (result)

async def checkMinecraftAccaunt(tgId):
    async with async_session() as session:
        _user = await session.scalar(select(user).where(user.tgId == tgId))
        _minecraftUser = await session.scalar(select(userMinecraft).where(userMinecraft.botTelegramUser_id == _user.id))
        try:
            return(_minecraftUser.name)
        except:
            return(None)

async def supportSend(tgId, name):
    async with async_session() as session:
        try:
            _user = await session.scalar(select(user).where(user.tgId == tgId))
            session.add(support(name=name, botTelegramUser_id=_user.id))
            await session.commit()
            await bot.send_message(int(ADMIN_ID), "Новое обращение!")
            return("Обращение успешно отправлено.")
        except:
            return("Ошибка! Попробуйте позже...")

async def checkBanned(tgId):
    async with async_session() as session:
        try:
            _user = await session.scalar(select(user).where(user.tgId == tgId))
            return(_user.notBanned)
        except:
            return(True)

async def getReward(tgId):
    async with async_session() as session:
        try:
            _user = await session.scalar(select(user).where(user.tgId == tgId))
            if (_user.reward == False):
                _mineUser = await session.scalar(select(userMinecraft).where(userMinecraft.botTelegramUser_id == _user.id))
                textCommand = await commands.getRewardVip(_mineUser.name)
                await command(textCommand)
                await session.execute(update(user).values(reward= True).where(user.id == _user.id))
                await session.commit()
                return "Награда успешно получена."
            else:
                return "Награда уже была получена."
        except:
            return "Ошибка. Попробуйте позже..."

async def getAllSupportMessageNoCheck():
    async with async_session() as session:
        supports=[]
        allSupports = await session.scalars(select(support).where(support.check == False))
        for sp in allSupports:
            supports.append(sp.id)
        return(supports)

async def getSupportForId(id):
    async with async_session() as session:
        _support = await  session.scalar(select(support).where(support.id == id))
        _user = await  session.scalar(select(user).where(user.id == _support.botTelegramUser_id))
        return(_support.name, _support.id)

async def sendSupportResponse(id, text):
    async with async_session() as session:
        try:
            _support = await  session.scalar(select(support).where(support.id == id))
            _user = await  session.scalar(select(user).where(user.id == _support.botTelegramUser_id))
            await bot.send_message(_user.tgId, f"Ответ на Ваше обращение:\n{text}")
            await session.execute(update(support).values(check=True).where(support.id == id))
            await session.commit()
            return("Ответ успешно отправлен!")
        except:
            return "Ошибка. Попробуйте позже."

async def sendAllMessageRes(text):
    async with async_session() as session:
        #try:
            _users = await session.scalars(select(user))
            for _user in _users:
                try:
                    await bot.send_message(_user.tgId, text)
                except:
                    pass
            return "Готово"
        #except:
        #    return "Ошибка"

async def allUsers():
    async with async_session() as session:
        #try:
            _users = await session.scalars(select(user))
            col = 0
            for _user in _users:
                col+=1
            return col