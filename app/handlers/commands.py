import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command


from app.handlers.user_private import menu_keyboard, show_details


cmd_router = Router()

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
    await message.answer("Спасибо за ваш отзыв!", reply_markup=menu_keyboard)
    
    
@cmd_router.message(Command("faq"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Здесь будет список вопросов", reply_markup=menu_keyboard)
    
    
@cmd_router.message(Command("contacts"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("По всем вопросам обращайтесь к моему создателю @bratisman", reply_markup=menu_keyboard)