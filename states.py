from aiogram.fsm.state import State, StatesGroup

class Conversation(StatesGroup):
    WAITING_FOR_LINK = State()
    WAITING_FOR_FORMAT = State()
