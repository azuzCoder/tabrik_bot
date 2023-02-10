from aiogram.dispatcher.filters.state import State, StatesGroup


class Birthday(StatesGroup):
    name = State()
    image_id = State()
    congrat = State()
    date = State()
    is_correct = State()
    chat_list = State()


class EditBirthday(StatesGroup):
    basic = State()
    name = State()
    image_id = State()
    congrat = State()
    date = State()
