from services.user import user_add, get_user_by_tg
from services.data import save_user_action
from utils.states import ProcessLLMStates
from database.database import get_db

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from utils.texts import SystemTexts
from utils.path import get_image_path
from aiogram.types import FSInputFile
from models import Company

router = Router()
session = get_db()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    save_user_action(session, "start", user.id)
    msg = SystemTexts.START_MESSAGE
    await message.answer(msg)
    await cmd_bot(message, state)


@router.message(Command("feedback"))
async def reviews_info(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "feedback", user.id)
    msg = SystemTexts.FEEDBACK_MESSAGE
    await message.answer(msg)


@router.message(Command("help"))
async def widget_info(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "help", user.id)
    msg = SystemTexts.START_MESSAGE
    await message.answer(msg)


# @router.message(Command("chat"))
# async def cmd_bot(message: Message, state: FSMContext):
#     user = get_user_by_tg(session, message.from_user.id)
#     if user is None:
#         user_add(session, message.from_user.id)
#     save_user_action(session, "chat", user.id)
#     msg = SystemTexts.CHAT_MESSAGE
#     await message.answer(msg)
#     await state.set_state(ProcessLLMStates.waitForText)


@router.message(Command("chat"))
async def cmd_bot(message: Message, state: FSMContext):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    save_user_action(session, "chat", user.id)

    # Получаем список компаний
    companies = session.query(Company).all()
    if not companies:
        await message.answer("Нет доступных компаний для выбора.")
        return

    # Генерируем инлайн-клавиатуру для выбора компании
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=company.name, callback_data=f"select_company_{company.id}")]
            for company in companies
        ]
    )

    await message.answer("Выберите компанию:", reply_markup=keyboard)


@router.callback_query(lambda callback: callback.data.startswith("select_company_"))
async def select_company(callback_query: CallbackQuery, state: FSMContext):
    # Извлекаем ID компании из callback_data
    company_id = callback_query.data.split("_")[-1]
    selected_company = session.query(Company).filter_by(id=company_id).first()

    if not selected_company:
        await callback_query.answer("Компания не найдена. Попробуйте снова.", show_alert=True)
        return

    # Сохраняем выбранную компанию в состоянии
    await state.update_data(company_name=selected_company.name)

    await callback_query.message.answer(
        f"Вы выбрали компанию: {selected_company.name}\nТеперь введите ваш вопрос."
    )
    await state.set_state(ProcessLLMStates.waitForText)
    await callback_query.answer()


async def send_contact_info(message_or_query):
    msg = SystemTexts.CONTACT_MANAGER
    if isinstance(message_or_query, Message):  # Если вызвано через команду
        await message_or_query.answer(msg)
    elif isinstance(message_or_query, CallbackQuery):  # Если вызвано через кнопку
        await message_or_query.message.answer(msg)
        await message_or_query.answer()  # Для закрытия всплывающего окна


@router.message(Command("call"))
async def cmd_call(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    save_user_action(session, "call", user.id)
    await send_contact_info(message)


@router.message(Command("widget"))
async def cmd_widget(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "widget", user.id) #TODO? возможно в остл шагах виджета

    await message.answer(SystemTexts.START_WIDGET_MESSAGE)
    await message.answer(SystemTexts.WIDGET_INTRO_MESSAGE)
    await message.answer(SystemTexts.FIRST_SERVICE_MESSAGE)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Презентация Отзывы", callback_data="presentation_feedback"
                ),
                InlineKeyboardButton(
                    text="Презентация Виджет", callback_data="presentation_widget"
                ),
            ],
            [InlineKeyboardButton(text="Пощупать аналитику", callback_data="analytics_demo")],
        ]
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "presentation_feedback")
async def presentation_feedback(callback_query: CallbackQuery):
    await callback_query.message.answer(SystemTexts.PRESENTATION_FEEDBACK_MESSAGE)

    image_path = get_image_path("image_1.png")
    photo = FSInputFile(image_path)
    await callback_query.message.answer_photo(photo=photo)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Интерактивная презентация", callback_data="interactive_feedback_start"),
                InlineKeyboardButton(text="Скачать презентацию", callback_data="download_feedback"),
            ]
        ]
    )
    await callback_query.message.answer(SystemTexts.FEEDBACK_SOLUTION_DETAILS, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "download_feedback")
async def download_feedback(callback_query: CallbackQuery):
    pdf_path = get_image_path("Презентация_Napoleon_IT_Отзывы.pdf")
    pdf_file = FSInputFile(pdf_path)
    await callback_query.message.answer_document(pdf_file)
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "interactive_feedback_start")
async def interactive_feedback_start(callback_query: CallbackQuery):
    await callback_query.message.answer(SystemTexts.INTERACTIVE_FEEDBACK_START_MESSAGE)

    await callback_query.message.answer(SystemTexts.INTERACTIVE_PRESENTATION_TRENDS)

    image_path = get_image_path("image_1.png")
    photo = FSInputFile(image_path)
    await callback_query.message.answer_photo(photo=photo)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Продолжить", callback_data="feedback_step_1"),
                InlineKeyboardButton(text="Скачать презентацию", callback_data="download_feedback"),
            ]
        ]
    )
    await callback_query.message.answer("Что дальше?", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("feedback_step_"))
async def interactive_feedback_steps(callback_query: CallbackQuery):
    steps = [
        ("feedback_step_1", SystemTexts.INTERACTIVE_PRESENTATION_TRENDS, get_image_path("image_3.png")),
        ("feedback_step_2", SystemTexts.INTERACTIVE_ALERT_SYSTEM, get_image_path("image_4.png")),
        ("feedback_step_3", SystemTexts.INTERACTIVE_OPERATIONAL_REPORTS, get_image_path("image_5.png")),
        ("feedback_step_4", SystemTexts.INTERACTIVE_STRATEGIC_REPORTS, get_image_path("image_6.png")),
        ("feedback_step_5", SystemTexts.INTERACTIVE_AUTO_RESPONSES, get_image_path("image_7.png")),
        ("feedback_step_6", SystemTexts.INTERACTIVE_SEO, get_image_path("image_8.png")),
    ]

    current_step = callback_query.data

    for idx, (step_id, text, image_url) in enumerate(steps):
        if current_step == step_id:
            await callback_query.message.answer(text)

            image_path = get_image_path(image_url)
            photo = FSInputFile(image_path)
            await callback_query.message.answer_photo(photo=photo)

            if idx + 1 < len(steps):
                next_step = steps[idx + 1][0]
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Продолжить", callback_data=next_step
                            )
                        ]
                    ]
                )
                await callback_query.message.answer("Продолжим?", reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Изучить кейсы", callback_data="case_studies"),
                            InlineKeyboardButton(text="Пощупать аналитику", callback_data="analytics_demo"),
                        ],
                        [InlineKeyboardButton(text="Связаться с менеджером", callback_data="call_manager")],
                    ]
                )
                await callback_query.message.answer("Что вы хотите сделать дальше?", reply_markup=keyboard)
            break


@router.callback_query(lambda c: c.data == "call_manager")
async def callback_call_manager(callback_query: CallbackQuery):
    user = get_user_by_tg(session, callback_query.from_user.id)
    if user is None:
        user_add(session, callback_query.from_user.id)
    save_user_action(session, "call", user.id)
    await send_contact_info(callback_query)


@router.callback_query(lambda c: c.data == "case_studies")
async def case_studies(callback_query: CallbackQuery):
    await callback_query.message.answer(SystemTexts.CASE_STUDIES_INTRO)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Бренд одежды", callback_data="case_clothing"),
                InlineKeyboardButton(text="Ватная продукция", callback_data="case_cotton"),
            ],
            [
                InlineKeyboardButton(text="Натуральные лимонады", callback_data="case_lemonade"),
                InlineKeyboardButton(text="Магазин косметики", callback_data="case_cosmetics"),
            ],
        ]
    )
    await callback_query.message.answer("Выберите кейс:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("case_"))
async def specific_case(callback_query: CallbackQuery):
    case_name = callback_query.data.split("_")[1]
    await callback_query.message.answer(f"Подробности кейса: {case_name}")


@router.callback_query(lambda c: c.data == "presentation_widget")
async def widget_presentation(callback_query: CallbackQuery):
    await callback_query.message.answer(SystemTexts.WIDGET_INTRO)

    image_path = get_image_path("image_9.png")
    photo = FSInputFile(image_path)
    await callback_query.message.answer_photo(photo=photo)

    await callback_query.message.answer(SystemTexts.WIDGET_DESCRIPTION)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изучить кейсы", callback_data="case_studies"),
                InlineKeyboardButton(text="Связаться с менеджером", callback_data="call_manager"),
            ]
        ]
    )
    await callback_query.message.answer("Выберите действие:", reply_markup=keyboard)
    await callback_query.answer()

