import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.reply import get_keyboard
from app.database.dao import orm_add_user

start_keyboard = get_keyboard(
    "👍Конечно",
    "➡️Позже",
    placeholder="Выберите действие",
    sizes=(2,)
)

menu_keyboard = get_keyboard(
    "🔠Найти рецепт блюда по названию",
    "💛Подобрать рецепт по предпочтениям",
    "🥩Подобрать рецепт по ингредиентам",
    placeholder="Выберите действие",
    sizes=(1, 1, 1)
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
    await message.answer(f"Поехали! Много-много лет я провел, изучая исскуство кулинарии.\n" +
                         f"Теперь я готов поделиться с тобой своим опытом!\n\n" +
                         f"Вот что я могу сделать:\n\n" +
                         f"<b>🔠 ПРЕДОСТАВИТЬ ВАМ РЕЦЕПТ БЛЮДА ПО НАЗВАНИЮ</b>\n" +
                         f"Вы вводите название блюда, я выдаю вам список необходимых ингредиентов и пошаговую инструкцию приготовления\n\n" +
                         f"<b>💛 ПОДОБРАТЬ СЛУЧАЙНЫЙ РЕЦЕПТ ПО ВАШИМ ВКУСОВЫМ ПРЕДПОЧТЕНИЯМ</b>\n" +
                         f"Вы указываете ваши пожелания (например, 'Хочу дессерт с бананом и шоколадом'), а я нахожу рецепт, выдаю вам список необходимых ингридиентов и пошаговую инструкцию приготовления\n\n" +
                         f"<b>🥩 ПОДОБРАТЬ РЕЦЕПТ ПО ИНГРЕДИЕНТАМ, КОТОРЫЕ У ВАС ЕСТЬ В ХОЛОДИЛЬНИКЕ</b>\n" +
                         f"Вы указываете список доступных вам ингредиентов, а я придумываю рецепт и выдаю вам пошаговую инструкцию приготовления\n\n\n", 
                         reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await message.answer(f'🧠 <b>ВАЖНО!</b> Я спроектирован на основе генеративного исскуственного интеллекта (GPT)\n' +
                         f'Поэтому прошу ипользовать корректные имена ингредиентов и рецептов, чтобы я понял вас.\n\n' +
                         f'🤖 <b>P.S.</b> Я все еще нахожусь в состоянии разработки, так что возможны неполадки в работе, особенно в процессе генерации рецептов\n\n')
    await message.answer("🔥 Приятного времяпрепровождения! И конечно же приятного аппетита!", 
                                 reply_markup=menu_keyboard)
    
    
@user_private_router.message(F.text.casefold() == "➡️позже")
async def to_menu(message: Message):
    await message.answer(f"🔥 Тогда перейдем сразу к делу!\n\n" +
                         f"Итак, что я могу для вас сделать?", reply_markup=menu_keyboard)
    
    
@user_private_router.message()
async def incorrect_message(message: Message):
    await message.answer("Извините, я не понимаю")
    await message.answer(f'id чата: {message.chat.id}')