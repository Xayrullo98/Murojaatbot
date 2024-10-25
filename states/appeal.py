from aiogram.dispatcher.filters.state import State,StatesGroup


class AppealState(StatesGroup):
    name = State()
    last_name = State()
    phone = State()
    appeal = State()
    confirm = State()


class AdminState(StatesGroup):
    name = State()
    tg_id = State()