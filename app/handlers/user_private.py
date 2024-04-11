import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.reply import get_keyboard
from app.database.dao import orm_add_user
from app.common.texts import menu_text, about_info

start_keyboard = get_keyboard(
    "👍Конечно",
    "➡️Позже",
    placeholder="Выберите действие",
    sizes=(2,)
)

menu_keyboard = get_keyboard(
    "1",
    "2",
    "3",
    placeholder="Выберите действие",
    sizes=(3, )
)


user_private_router = Router()

@user_private_router.message(CommandStart())
async def command_start(message: Message, session: AsyncSession):
    await message.answer_sticker("CAACAgIAAxkBAAIQpWYU9mtrJiFzeDz638kyo_vHiWj0AAKwCwACLw_wBrvBiwJ7mTB8NAQ", 
                                 reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await message.answer(f"🤖Бонжур, <b>{message.from_user.full_name}</b>! Я Папийон, ваш кулинарный AI ассистент!")
    await orm_add_user(session, user_id=message.from_user.id, user_name=message.from_user.full_name)
    await message.answer("Мне не терпится рассказать о себе, что скажете?", reply_markup=start_keyboard)


@user_private_router.message(F.text.casefold() == "👍конечно")
async def show_details(message: Message):
    await message.answer(about_info, reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await message.answer("🔥 Приятного времяпрепровождения! И конечно же приятного аппетита!")
    await message.answer(menu_text, reply_markup=menu_keyboard)
    
    
@user_private_router.message(F.text.casefold() == "➡️позже")
async def to_menu(message: Message):
    await message.answer(f"🔥 Тогда перейдем сразу к делу!\n\n")
    await message.answer(menu_text, reply_markup=menu_keyboard)
    
    
@user_private_router.message()
async def incorrect_message(message: Message):
    await message.answer("Извините, я не понимаю (внимательно следуйте инструкциям, либо используйте кнопки снизу)")