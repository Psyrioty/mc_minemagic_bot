from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

mainNoAuth = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Привязка к персонажу 📲', callback_data='connect')],
                            [InlineKeyboardButton(text='Жалоба на игрока ❗️', callback_data='report'), InlineKeyboardButton(text='Тех. поддержка ❓', callback_data='support')],
                            [InlineKeyboardButton(text='Сотрудничество 🤝', callback_data='cooperation'), InlineKeyboardButton(text='Пожелания 💭', callback_data='wish')]
])

mainAuth = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Получить награду за привязку 🎁', callback_data='reward')],
                            [InlineKeyboardButton(text='Ивент ✨', callback_data='event')],
                            [InlineKeyboardButton(text='Сменить пароль в игре 🔐', callback_data='newPassword')],
                            [InlineKeyboardButton(text='Жалоба на игрока ❗️', callback_data='report'), InlineKeyboardButton(text='Тех. поддержка ❓', callback_data='support')],
                            [InlineKeyboardButton(text='Сотрудничество 🤝', callback_data='cooperation'), InlineKeyboardButton(text='Пожелания 💭', callback_data='wish')]
])

event = toMain = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Получить семена 🎁', callback_data='giveEvent')],
                            [InlineKeyboardButton(text='В главное меню 🏠', callback_data='toMain')]
])

toMain = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='В главное меню 🏠', callback_data='toMain')]
])

