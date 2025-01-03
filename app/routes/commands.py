from services.user import user_add, get_user_by_tg
from services.data import save_user_action
from utils.states import ProcessLLMStates
from database.database import get_db

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from utils.texts import SystemTexts, SystemMessages
from utils.path import get_image_path
from utils.keyboards import inline_keyboards
from aiogram.types import FSInputFile
from models import Company

router = Router()
session = get_db()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
        user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "start", user.id)
    await message.answer(SystemTexts.START_MESSAGE_1)
    await message.answer(SystemTexts.START_MESSAGE_2)
    await message.answer(
        SystemTexts.START_MESSAGE_3, reply_markup=inline_keyboards.help()
    )


@router.message(Command("help"))
async def widget_info(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "help", user.id)
    await message.answer(SystemTexts.START_MESSAGE_1)
    await message.answer(SystemTexts.START_MESSAGE_2)
    await message.answer(
        SystemTexts.START_MESSAGE_3, reply_markup=inline_keyboards.help()
    )


@router.message(Command("chat"))
async def cmd_bot(message: Message):
    await init_chat(message)


@router.callback_query(lambda c: c.data == "chat")
async def callback_chat(callback_query: CallbackQuery):
    await init_chat(callback_query)


async def init_chat(message_or_query):
    user = get_user_by_tg(session, message_or_query.from_user.id)
    if user is None:
        user_add(session, message_or_query.from_user.id)
    save_user_action(session, "chat", user.id)

    companies = session.query(Company).all()
    if not companies:
        await message_or_query.answer(SystemMessages.NO_COMPANIES)
        return

    if isinstance(message_or_query, CallbackQuery):
        message_or_query = message_or_query.message

    await message_or_query.answer(
        SystemMessages.CHOOSE_COMPANY,
        reply_markup=inline_keyboards.select_company(companies),
    )


@router.callback_query(lambda c: c.data.startswith("select_company_"))
async def select_company(callback_query: CallbackQuery, state: FSMContext):
    # Извлекаем ID компании из callback_data
    company_id = callback_query.data.split("_")[-1]
    selected_company = session.query(Company).filter_by(id=company_id).first()

    if not selected_company:
        await callback_query.answer(SystemMessages.CANT_FOUND_COMPANY, show_alert=True)
        return

    # Сохраняем выбранную компанию в состоянии
    await state.update_data(company_name=selected_company.name)

    await callback_query.message.answer(
        SystemMessages.CHOSEN_COMPANY + selected_company.name
    )
    await callback_query.message.answer(SystemMessages.QUESTION_ASKING)
    await state.set_state(ProcessLLMStates.waitForText)


@router.message(Command("call"))
async def cmd_call(message: Message):
    await send_contact_info(message)


@router.callback_query(lambda c: c.data == "call_manager")
async def callback_call_manager(callback_query: CallbackQuery):
    await send_contact_info(callback_query)


async def send_contact_info(message_or_query):
    user = get_user_by_tg(session, message_or_query.from_user.id)
    if user is None:
        user_add(session, message_or_query.from_user.id)
    save_user_action(session, "call", user.id)

    msg = SystemTexts.CONTACT_MANAGER
    if isinstance(message_or_query, CallbackQuery):  # Если вызвано через кнопку

        message_or_query = message_or_query.message

    await message_or_query.answer(msg)


@router.message(Command("widget"))
async def cmd_widget(message: Message):
    await widget_info(message)


@router.callback_query(lambda c: c.data == "presentation_widget")
async def widget_presentation(callback_query: CallbackQuery):
    await widget_info(callback_query)


async def widget_info(message_or_query):
    user = get_user_by_tg(session, message_or_query.from_user.id)
    save_user_action(session, "widget", user.id)
    if isinstance(message_or_query, CallbackQuery):  # Если вызвано через кнопку

        message_or_query = message_or_query.message

    image_path = get_image_path("image_9.png")
    photo = FSInputFile(image_path)
    await message_or_query.answer_photo(photo=photo)
    await message_or_query.answer(
        SystemTexts.WIDGET_INTRO, reply_markup=inline_keyboards.call_manager()
    )


@router.callback_query(lambda c: c.data == "case_studies")
async def case_studies(callback_query: CallbackQuery):

    await callback_query.message.answer(
        SystemTexts.CASE_STUDIES_INTRO, reply_markup=inline_keyboards.cases()
    )


@router.callback_query(lambda c: c.data.startswith("case_"))
async def specific_case(callback_query: CallbackQuery):
    case_name = callback_query.data.split("_")[1]
    image_1_path = get_image_path("1.jpg", f"widget/{case_name}")
    image_2_path = get_image_path("2.jpg", f"widget/{case_name}")
    photo_1 = FSInputFile(image_1_path)
    photo_2 = FSInputFile(image_2_path)

    await callback_query.message.answer_photo(photo=photo_1)
    await callback_query.message.answer_photo(
        photo=photo_2,
        reply_markup=inline_keyboards.cases_after_pressing(callback_query.data),
    )


@router.message(Command("feedback"))
async def reviews_info(message: Message):
    await feedback_info(message)


@router.callback_query(lambda c: c.data == "presentation_feedback")
async def presentation_feedback(callback_query: CallbackQuery):

    await feedback_info(callback_query)


async def feedback_info(message_or_query):
    user = get_user_by_tg(session, message_or_query.from_user.id)
    save_user_action(session, "feedback", user.id)
    if isinstance(message_or_query, CallbackQuery):  # Если вызвано через кнопку
        message_or_query = message_or_query.message
    image_path = get_image_path("image_1.png")
    photo = FSInputFile(image_path)
    await message_or_query.answer_photo(photo=photo)
    await message_or_query.answer(
        SystemTexts.FEEDBACK_SOLUTION_DETAILS,
        reply_markup=inline_keyboards.feedback_look_or_download(),
    )


@router.callback_query(lambda c: c.data == "download_feedback")
async def download_feedback(callback_query: CallbackQuery):
    pdf_path = get_image_path("Презентация_Napoleon_IT_Отзывы.pdf")
    pdf_file = FSInputFile(pdf_path)

    await callback_query.message.answer_document(pdf_file)
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "interactive_feedback_start")
async def interactive_feedback_start(callback_query: CallbackQuery):
    image_path = get_image_path("image_1.png")
    photo = FSInputFile(image_path)

    await callback_query.message.answer(SystemTexts.INTERACTIVE_FEEDBACK_START_MESSAGE)
    await callback_query.message.answer_photo(photo=photo)
    await callback_query.message.answer(
        SystemTexts.INTERACTIVE_FEEDBACK_START_DETAILS,
        reply_markup=inline_keyboards.feedback_step_1(),
    )


@router.callback_query(lambda c: c.data.startswith("feedback_step_"))
async def interactive_feedback_steps(callback_query: CallbackQuery):

    steps = [
        (
            "feedback_step_1",
            SystemTexts.INTERACTIVE_FEEDBACK_IMAGE_2,
            get_image_path("image_2.png"),
        ),
        (
            "feedback_step_2",
            SystemTexts.INTERACTIVE_FEEDBACK_IMAGE_3,
            get_image_path("image_3.png"),
        ),
        (
            "feedback_step_3",
            SystemTexts.INTERACTIVE_FEEDBACK_IMAGE_4,
            get_image_path("image_4.png"),
        ),
        (
            "feedback_step_4",
            SystemTexts.INTERACTIVE_FEEDBACK_IMAGE_5,
            get_image_path("image_5.png"),
        ),
        (
            "feedback_step_5",
            SystemTexts.INTERACTIVE_FEEDBACK_IMAGE_6,
            get_image_path("image_6.png"),
        ),
        (
            "feedback_step_6",
            SystemTexts.INTERACTIVE_FEEDBACK_IMAGE_7,
            get_image_path("image_7.png"),
        ),
        (
            "feedback_step_7",
            SystemTexts.INTERACTIVE_FEEDBACK_IMAGE_8,
            get_image_path("image_8.png"),
        ),
    ]

    current_step = callback_query.data

    for idx, (step_id, text, image_url) in enumerate(steps):
        if current_step == step_id:

            image_path = get_image_path(image_url)
            photo = FSInputFile(image_path)
            await callback_query.message.answer_photo(photo=photo)

            if idx + 1 < len(steps):
                next_step = steps[idx + 1][0]
                await callback_query.message.answer(
                    text, reply_markup=inline_keyboards.next_step(next_step)
                )
            else:
                await callback_query.message.answer(text)
                await callback_query.message.answer(
                    SystemMessages.END_MESSAGE,
                    reply_markup=inline_keyboards.case_or_manager(),
                )
            break
