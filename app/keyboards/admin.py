from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import getAllSupportMessageNoCheck

mainAdmin = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Посмотреть неотвеченные обращения', callback_data='checkSupport')],
                            [InlineKeyboardButton(text='Забанить пользователя по ID', callback_data='ban')],
                            [InlineKeyboardButton(text='Рассылка', callback_data='sendAllUsersMessage')]
])

async def getSupports():
    allSupports = await getAllSupportMessageNoCheck()
    keyboard = InlineKeyboardBuilder()
    for support in allSupports:
        keyboard.add(InlineKeyboardButton(text=f"Обращение ID: {support}",
                                          callback_data=f'support_{support}'))
    return keyboard.adjust(2).as_markup()

async def btnResponse(supId):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=f"Ответить",
                                          callback_data=f'responseSupport_{supId}'))
    return keyboard.adjust(2).as_markup()