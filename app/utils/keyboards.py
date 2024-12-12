from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from config import CommonQuestions


# Кнопки инлайн клавиатуры в поле чата
def get_common_questions_keyboard():
    keyboard_buttons = [
        [InlineKeyboardButton(text=question, callback_data=question)]
        for question in CommonQuestions.QUESTION_ANSWERS.keys()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard
