from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.state import sendVerificationKey
from app.rconConnector import sendCode
from app.database.requests import setTelegramUser, setVerificationCode

import app.keyboards.base as kb

router = Router()


@router.message(Command('start', 'restart'))
@router.callback_query(F.data == 'toMain')
async def cmd_start(message: Message | CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} выполнил команду /start")
    if isinstance(message, Message):
        await setTelegramUser(message.from_user.id, message.from_user.username)
        await message.answer(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainNoAuth)
    else:
        await state.clear()
        await message.message.edit_text(text='Привет, {0}!'.format(message.from_user.first_name), reply_markup=kb.mainNoAuth)

@router.callback_query(F.data == 'connect')
async def connect(callback: CallbackQuery, state: FSMContext):
    print(f"Пользователь ID: {callback.from_user.id} USERNAME: {callback.from_user.username} нажал кнопку: {callback.data}")
    await callback.message.edit_text(f'Введите Ваш ник.\nЧтобы получить код, игрок должен быть в сети на сервере: Выживание.', reply_markup=kb.toMain)
    await state.set_state(sendVerificationKey.name)


@router.message(sendVerificationKey.name)
async def sendVerificationCodeName(message: Message):
    print(f"Пользователь ID: {message.from_user.id} USERNAME: {message.from_user.username} ввел ник: {message.text}")
    name = message.text
    code = await  setVerificationCode(message.from_user.id)
    await sendCode(name, code)