from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from app.state import adminResponseSupport, adminSendAll
from app.database.requests import getSupportForId, sendSupportResponse, sendAllMessageRes, allUsers
from config import ADMIN_ID

import app.keyboards.admin as kb

routerAdmin = Router()

class ControlProtect(Filter):
    async def __call__(self, message: Message):
        me = message.from_user
        if(me.id == int(ADMIN_ID)):
            return True

#ЗАПУСК БОТА АДМИНКА
@routerAdmin.message(ControlProtect(), Command('admin'))
async def cmd_start(message: Message | CallbackQuery, state: FSMContext):
    await message.answer(text='Админ панель', reply_markup=kb.mainAdmin)

#ПРОСМОТР ОБРАЩЕНИЙ
@routerAdmin.callback_query(ControlProtect(), F.data == 'checkSupport')
async def checkSupport(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'Неотвеченные обращения:', reply_markup=await kb.getSupports())

@routerAdmin.callback_query(ControlProtect(), F.data.startswith('support_'))
async def supportClick(callback: CallbackQuery):
    support = await getSupportForId(int(callback.data.split('_')[1]))
    text = support[0]
    supportId = support[1]
    await callback.message.edit_text(text= text, reply_markup=await kb.btnResponse(supportId), parse_mode='HTML')

@routerAdmin.callback_query(ControlProtect(), F.data.startswith('responseSupport_'))
async def supportResponse(callback: CallbackQuery, state: FSMContext):
    oldText = callback.message.text
    await callback.message.edit_text(text=f"Ответ на обращение:\n{oldText}", parse_mode='HTML')
    await state.set_state(adminResponseSupport.text)
    await state.update_data(supportId = int(callback.data.split('_')[1]))

@routerAdmin.message(ControlProtect(), adminResponseSupport.text)
async def supportResponseText(message: Message, state: FSMContext):
    stateData = await state.get_data()
    supportId = stateData['supportId']
    resultText = await sendSupportResponse(supportId, message.text)
    await message.answer(text=resultText)
    await state.clear()

#РАССЫЛКА
@routerAdmin.callback_query(ControlProtect(), F.data == 'sendAllUsersMessage')
async def sendAllMessage(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'Введите сообщение:')
    await state.set_state(adminSendAll.text)

@routerAdmin.message(ControlProtect(), adminSendAll.text)
async def sendAllText(message: Message, state: FSMContext):
    resultText = await sendAllMessageRes(message.text)
    await message.answer(text=resultText)
    await state.clear()


#пользователи
@routerAdmin.callback_query(ControlProtect(), F.data == 'users')
async def colUsers(callback: CallbackQuery):
    col = await allUsers()
    await callback.message.edit_text(f'Колич. пользователей: {col}')