from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from config import CommonQuestions


# Кнопки стандартной клавиатуры под строкой ввода
# def get_common_questions_keyboard():
#     keyboard_buttons = [
#         [KeyboardButton(text=question)]
#         for question in CommonQuestions.QUESTION_ANSWERS.keys()
#     ]
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=keyboard_buttons, resize_keyboard=True, one_time_keyboard=True
#     )
#     return keyboard

# Кнопки инлайн клавиатуры в поле чата
def get_common_questions_keyboard():
    keyboard_buttons = [
        [InlineKeyboardButton(text=question, callback_data=question)]
        for question in CommonQuestions.QUESTION_ANSWERS.keys()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard
