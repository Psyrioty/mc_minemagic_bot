from aiogram.fsm.state import State, StatesGroup


class sendVerificationKey(StatesGroup):
    name = State()
    code = State()

class report(StatesGroup):
    name = State()
    badName = State()
    text = State()

class support(StatesGroup):
    name = State()
    text = State()

class cooperation(StatesGroup):
    text = State()

class wish(StatesGroup):
    text = State()

class setNewPassword(StatesGroup):
    password = State()

class adminResponseSupport(StatesGroup):
    text = State()

class adminSendAll(StatesGroup):
    text = State()