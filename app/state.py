from aiogram.fsm.state import State, StatesGroup


class sendVerificationKey(StatesGroup):
    name = State()