from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from utils.texts import ButtonsTexts
from config import CommonQuestions


# Кнопки инлайн клавиатуры в поле чата
class Keyboards:
    def common_questions():
        keyboard_buttons = [
            [InlineKeyboardButton(text=question, callback_data=question)]
            for question in CommonQuestions.QUESTION_ANSWERS.keys()
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard

    def help():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.FEEDBACK_PRESENTATION,
                        callback_data="presentation_feedback",
                    ),
                    InlineKeyboardButton(
                        text=ButtonsTexts.WIDGET_PRESENTATION,
                        callback_data="presentation_widget",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.QUESTION_ASKING, callback_data="chat"
                    )
                ],
            ]
        )
        return keyboard

    def next_step(next_step):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.NEXT_STEP, callback_data=next_step
                    )
                ]
            ]
        )
        return keyboard

    def case_or_manager():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.VIEW_CASES, callback_data="case_studies"
                    ),
                    InlineKeyboardButton(
                        text=ButtonsTexts.QUESTION_ASKING,
                        callback_data="chat",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.CALL_MANAGER,
                        callback_data="call_manager",
                    )
                ],
            ]
        )
        return keyboard

    def call_manager():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.CALL_MANAGER,
                        callback_data="call_manager",
                    )
                ],
            ]
        )
        return keyboard

    def feedback_step_1():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.NEXT_STEP, callback_data="feedback_step_1"
                    ),
                    InlineKeyboardButton(
                        text=ButtonsTexts.DOWNLOAD_PRESENTATION,
                        callback_data="download_feedback",
                    ),
                ]
            ]
        )
        return keyboard

    def feedback_look_or_download():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=ButtonsTexts.INTERACTIVE_PRESENTATION,
                        callback_data="interactive_feedback_start",
                    ),
                    InlineKeyboardButton(
                        text=ButtonsTexts.CALL_MANAGER,
                        callback_data="download_feedback",
                    ),
                ]
            ]
        )
        return keyboard

    def cases():
        buttons = [
            [InlineKeyboardButton(text=ButtonsTexts.CASE_OD, callback_data="case_od")],
            [InlineKeyboardButton(text=ButtonsTexts.CASE_VT, callback_data="case_vt")],
            [InlineKeyboardButton(text=ButtonsTexts.CASE_LI, callback_data="case_li")],
            [InlineKeyboardButton(text=ButtonsTexts.CASE_KO, callback_data="case_ko")],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    def cases_after_pressing(pressed_button):
        buttons = [
            InlineKeyboardButton(text=ButtonsTexts.CASE_OD, callback_data="case_od"),
            InlineKeyboardButton(text=ButtonsTexts.CASE_VT, callback_data="case_vt"),
            InlineKeyboardButton(text=ButtonsTexts.CASE_LI, callback_data="case_li"),
            InlineKeyboardButton(text=ButtonsTexts.CASE_KO, callback_data="case_ko"),
            InlineKeyboardButton(
                text=ButtonsTexts.CALL_MANAGER,
                callback_data="call_manager",
            ),
            InlineKeyboardButton(
                text=ButtonsTexts.QUESTION_ASKING, callback_data="chat"
            ),
        ]
        remaining_buttons = [
            [btn] for btn in buttons if btn.callback_data != pressed_button
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=remaining_buttons)

        return keyboard

    def select_company(companies):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=company.name, callback_data=f"select_company_{company.id}"
                    )
                ]
                for company in companies
            ]
        )
        return keyboard


inline_keyboards = Keyboards
