import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command


from app.handlers.user_private import menu_keyboard, show_details
from app.handlers.get_random_recipe import cancel_keyboard
from app.common.texts import feedback_text
from app.config import settings


cmd_router = Router()


class SendFeedback(StatesGroup):
    feedback = State()


@cmd_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Итак, что я могу для вас сделать?", reply_markup=menu_keyboard)
    
    
@cmd_router.message(Command("about"))
async def cmd_about(message: Message, state: FSMContext):
    await state.clear()
    await show_details(message)
    

@cmd_router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(feedback_text)
    await state.set_state(SendFeedback.feedback)
    await message.answer("✉️Напишите ваш отзыв", reply_markup=cancel_keyboard)
    
@cmd_router.message(StateFilter(SendFeedback.feedback), F.text == "Отмена")
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Итак, что я могу для вас сделать?", reply_markup=menu_keyboard)

@cmd_router.message(StateFilter(SendFeedback.feedback), F.text)
async def cmd_feedback(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await message.answer("Спасибо, отзыв был успешно отправлен!", reply_markup=menu_keyboard)
    
@cmd_router.message(StateFilter(SendFeedback.feedback))
async def cmd_feedback(message: Message, state: FSMContext):
    await message.answer("Неверный формат данных")

    
@cmd_router.message(Command("faq"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Здесь будет список вопросов", reply_markup=menu_keyboard)
    
    
@cmd_router.message(Command("contacts"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("По всем вопросам обращайтесь к моему создателю @bratisman", reply_markup=menu_keyboard)