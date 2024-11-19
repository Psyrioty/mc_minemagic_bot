from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext

from app.database.listData import jsonData

from app.tgBot import bot

from config import RCON_IP, RCON_PORT, RCON_PASSWORD, LOBBY_RCON_IP, LOBBY_RCON_PORT, LOBBY_RCON_PASSWORD, CHANNEL_ID

from app.keyboards.base import toMain
from app.state import sendVerificationKey, report, support, cooperation, wish, setNewPassword
from app.rconConnector import rconConnector
from app.database.requests import setTelegramUser, setVerificationCode, checkVerificationCode, checkMinecraftAccaunt, supportSend, checkBanned, getReward, getPlayerForTelegramID
from app.commands import commands

import app.keyboards.base as kb

router = Router()

class ControlProtect(Filter):
    async def __call__(self, message: Message):
        me = message.from_user
        res = await checkBanned(me.id)
        return res

#ЗАПУСК БОТА
@router.message(ControlProtect(), Command('start', 'restart'))
@router.callback_query(ControlProtect(), F.data == 'toMain')
async def cmd_start(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} выполнил команду /start")
    try:
        res = await checkMinecraftAccaunt(message.from_user.id)
    except:
        res = None
    if isinstance(message, Message):
        if(res == None):
            await setTelegramUser(message.from_user.id, message.from_user.username)
            await message.answer(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainNoAuth)
        else:
            await setTelegramUser(message.from_user.id, message.from_user.username)
            await message.answer(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainAuth)
    else:
        if(res == None):
            await message.message.edit_text(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainNoAuth)
        else:
            await message.message.edit_text(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainAuth)

#ПРИВЯЗКА АККАУНТА
@router.callback_query(ControlProtect(), F.data == 'connect')
async def connect(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} USERNAME: {callback.from_user.username} нажал кнопку: {callback.data}")
    await callback.message.edit_text(f'Введите Ваш ник.\nЧтобы получить код, игрок должен быть в сети на сервере: Выживание.', reply_markup=kb.toMain)
    await state.set_state(sendVerificationKey.name)


@router.message(ControlProtect(), sendVerificationKey.name)
async def sendVerificationCodeName(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел ник: {message.text}")
    name = message.text
    if(' ' in name):
        await message.answer(text='Ник указан неверно, укажите ник без пробелов', reply_markup=kb.toMain)
    else:
        code = await  setVerificationCode(message.from_user.id, name)
        if code != "":
            await rconConnector.sendCode(name, code, RCON_IP, RCON_PORT, RCON_PASSWORD)
            await state.update_data(name=message.text)
            await message.answer(text='Введите Ваш код верификации, который был отправлен в игру:', reply_markup=kb.toMain)
            await state.set_state(sendVerificationKey.code)
        else:
            await message.answer(text='Такой игрок уже привязан к tg аккаунту.', reply_markup=kb.toMain)
            await state.clear()

@router.message(ControlProtect(), sendVerificationKey.code)
async def sendVerificationCodeCode(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    result = await checkVerificationCode(message.from_user.id, message.text, name)
    await message.answer(
        text = result,
        reply_markup=kb.toMain)
    await state.clear()



#REPORT
@router.callback_query(ControlProtect(), F.data == 'report')
async def reportBtn(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} USERNAME: {callback.from_user.username} нажал кнопку: {callback.data}")
    name = await checkMinecraftAccaunt(callback.from_user.id)
    if(name == None):
        await callback.message.edit_text(f'Укажите Ваш ник:', reply_markup=kb.toMain)
        await state.set_state(report.name)
    else:
        await callback.message.edit_text(f'Укажите ник подозреваемого:', reply_markup=kb.toMain)
        await state.update_data(name = name)
        await state.set_state(report.badName)

@router.message(ControlProtect(), report.name)
async def sendReportName(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел ник в разделе REPORT: {message.text}")
    name = message.text
    if(' ' in name):
        await message.answer(text='Ник указан неверно, укажите ник без пробелов', reply_markup=kb.toMain)
    else:
        await message.answer(text='Укажите ник подозреваемого:', reply_markup=kb.toMain)
        await state.update_data(name = message.text)
        await state.set_state(report.badName)

@router.message(ControlProtect(), report.badName)
async def sendReportBadName(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел ник подозреваемого в разделе REPORT: {message.text}")
    name = message.text
    if(' ' in name):
        await message.answer(text='Ник указан неверно, укажите ник без пробелов', reply_markup=kb.toMain)
    else:
        await message.answer(text='Укажите все подробности нарушения:', reply_markup=kb.toMain)
        await state.update_data(badName = message.text)
        await state.set_state(report.text)


@router.message(ControlProtect(), report.text)
async def sendReportText(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел текст обращения REPORT: {message.text}")
    text = message.text
    stateData = await state.get_data()
    name = stateData['name']
    badName = stateData['badName']
    supportText = f"TelegramID: {message.from_user.id}\nUsername: {message.from_user.username}\nREPORT\nИгровой ник: {name}\nНик подозреваемого: {badName}\nТекст обращения: {text}"
    resultText = await supportSend(message.from_user.id, supportText)
    await message.answer(text=resultText, reply_markup=kb.toMain)
    await state.clear()

#SUPPORT
@router.callback_query(ControlProtect(), F.data == 'support')
async def supportBtn(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} USERNAME: {callback.from_user.username} нажал кнопку: {callback.data}")
    name = await checkMinecraftAccaunt(callback.from_user.id)
    if(name == None):
        await callback.message.edit_text(f'Укажите Ваш ник:', reply_markup=kb.toMain)
        await state.set_state(support.name)
    else:
        await callback.message.edit_text(f'Опишите Вашу проблему:', reply_markup=kb.toMain)
        await state.update_data(name = name)
        await state.set_state(support.text)

@router.message(ControlProtect(), support.name)
async def sendSupportName(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел ник в разделе SUPPORT: {message.text}")
    name = message.text
    if(' ' in name):
        await message.answer(text='Ник указан неверно, укажите ник без пробелов', reply_markup=kb.toMain)
    else:
        await message.answer(text='Укажите Вашу проблему:', reply_markup=kb.toMain)
        await state.update_data(name = message.text)
        await state.set_state(support.text)

@router.message(ControlProtect(), support.text)
async def sendSupportText(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел текст обращения SUPPORT: {message.text}")
    text = message.text
    stateData = await state.get_data()
    name = stateData['name']
    supportText = f"TelegramID: {message.from_user.id}\nUsername: {message.from_user.username}\nSUPPORT\nИгровой ник: {name}\nТекст обращения: {text}"
    resultText = await supportSend(message.from_user.id, supportText)
    await message.answer(text=resultText, reply_markup=kb.toMain)
    await state.clear()

#СОТРУДНИЧЕСТВО
@router.callback_query(ControlProtect(), F.data == 'cooperation')
async def cooperationBtn(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} USERNAME: {callback.from_user.username} нажал кнопку: {callback.data}")
    await callback.message.edit_text(f'Напишите свое предложение по сотрудничеству:', reply_markup=kb.toMain)
    await state.set_state(cooperation.text)

@router.message(ControlProtect(), cooperation.text)
async def sendCooperationText(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел текст обращения COOPERATION: {message.text}")
    text = message.text
    supportText = f"TelegramID: {message.from_user.id}\nUsername: {message.from_user.username}\nCOOPERATION\nТекст обращения: {text}"
    resultText = await supportSend(message.from_user.id, supportText)
    await message.answer(text=resultText, reply_markup=kb.toMain)
    await state.clear()

#ПОЖЕЛАНИЕ
@router.callback_query(ControlProtect(), F.data == 'wish')
async def cooperationBtn(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} USERNAME: {callback.from_user.username} нажал кнопку: {callback.data}")
    await callback.message.edit_text(f'Напишите свое пожелание:', reply_markup=kb.toMain)
    await state.set_state(wish.text)

@router.message(ControlProtect(), wish.text)
async def sendCooperationText(message: Message, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел текст обращения WISH: {message.text}")
    text = message.text
    supportText = f"TelegramID: {message.from_user.id}\nUsername: {message.from_user.username}\nWISH\nТекст обращения: {text}"
    resultText = await supportSend(message.from_user.id, supportText)
    await message.answer(text=resultText, reply_markup=kb.toMain)
    await state.clear()

#ПОЛУЧЕНИЕ НАГРАДЫ
@router.callback_query(ControlProtect(), F.data == 'reward')
async def cooperationBtn(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} REWARD: {callback.from_user.username} нажал кнопку: {callback.data}")
    res = await getReward(callback.from_user.id)
    await callback.message.edit_text(res, reply_markup=kb.toMain)


#СМЕНА ПАРОЛЯ
@router.callback_query(ControlProtect(), F.data == 'newPassword')
async def newPassword(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} REWARD: {callback.from_user.username} нажал кнопку: {callback.data}")
    await callback.message.edit_text("Введите новый пароль без пробелов:", reply_markup=kb.toMain)
    await state.set_state(setNewPassword.password)

@router.message(ControlProtect(), setNewPassword.password)
async def newPasswordSend(message: Message, state: FSMContext):
    if(' ' in message.text):
        await message.answer("Введите новый пароль без пробелов:", reply_markup=kb.toMain)
    else:
        print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел новый пароль.")
        player = await getPlayerForTelegramID(message.from_user.id)
        password = message.text
        cmd = await commands.setNewPassword(password, player)
        res = await rconConnector.command(cmd, LOBBY_RCON_IP, LOBBY_RCON_PORT, LOBBY_RCON_PASSWORD)
        if (res):
            await message.answer(f"Запрос на новый пароль отправлен на сервер.\n Напоминание, если пароль очень простой или короткий, то сервер может его отклонить.", reply_markup=toMain)
        else:
            await message.answer("Ошибка. Попробуйте позже.",reply_markup=toMain)
        await state.clear()

#ИВЕНТ
@router.callback_query(ControlProtect(), F.data == 'event')
async def event(callback: CallbackQuery):
    name = await getPlayerForTelegramID(callback.from_user.id)
    data = jsonData()
    print(f"Пользователь ID: {callback.from_user.id} REWARD: {callback.from_user.username} нажал кнопку: {callback.data}")
    if (await data.checkUser(name) == None):
        inChannel = await bot.get_chat_member(chat_id= CHANNEL_ID, user_id= callback.from_user.id)
        if (inChannel.status != 'left'):
            text = f"<b><i>ИВЕНТ</i></b>\n\n<b><i><u>Инструкция:</u></i></b>\n\n1) Нажмите кнопку: `Получить семена 🎁`\n2) На игрового персонажа будут отправлены <u>семена</u>;\n3) Посадите семена на <u>своей территории</u> и дождитесь плода (убедитесь, что росток никто не раздавит, не зальет водой, а у плода будет место для появления);\n4) Плод будет похож на <u>алмазный блок</u>, сломайте его! (Плод появляется схоже с выращиванием тыквы и арбузом)"
            await callback.message.edit_text(text, reply_markup=kb.event, parse_mode="HTML")
        else:
            await callback.message.edit_text("Подпишитесь на канал: t.me/mc_minemagic!", reply_markup=kb.toMain, parse_mode="HTML")
    else:
        await callback.message.edit_text("Вы уже получали семена...", reply_markup=kb.toMain, parse_mode="HTML")

@router.callback_query(ControlProtect(), F.data == 'giveEvent')
async def giveEvent(callback: CallbackQuery):
    data = jsonData()
    playerName = await getPlayerForTelegramID(callback.from_user.id)
    if (await data.checkUser(playerName) == None):
        res = await rconConnector.command(f"ei give {playerName} fireSword 1", RCON_IP, RCON_PORT, RCON_PASSWORD)
        if (res):
            await data.addUser(playerName)
            await callback.message.edit_text("Семена отправлены на персонажа.", reply_markup=kb.toMain,
                                             parse_mode="HTML")
    else:
        await callback.message.edit_text("Вы уже получали семена...", reply_markup=kb.toMain,
                                         parse_mode="HTML")












#ЗАПУСК БОТА ОСТАЛЬНЫЕ СЛУЧАИ
@router.message(ControlProtect())
async def cmd_other(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} выполнил команду /start")
    res = await checkMinecraftAccaunt(message.from_user.id)
    if isinstance(message, Message):
        if(res == None):
            await setTelegramUser(message.from_user.id, message.from_user.username)
            await message.answer(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainNoAuth)
        else:
            await setTelegramUser(message.from_user.id, message.from_user.username)
            await message.answer(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainAuth)
    else:
        await state.clear()
        if(res == None):
            await message.message.edit_text(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainAuth)
        else:
            await message.message.edit_text(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainAuth)

#ЗАПУСК БОТА ЗАБАНЕНЫЙ АККАУНТ
@router.message()
@router.callback_query()
async def cmd_banned(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    await message.answer(text='Этот телеграм аккаунт забанен в боте!')