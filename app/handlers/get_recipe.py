from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command

from app.keyboards.reply import get_keyboard
from app.handlers.user_private import menu_keyboard
from app.handlers.get_random_recipe import cancel_keyboard
from app.services.gpt_free import generate_response

get_recipe_router = Router()

functional_keyboard = get_keyboard(
    "Найти еще рецепт",
    "Вернуться к меню",
    placeholder="Выберите действие", 
    sizes=(2,))

class RecipeDatails(StatesGroup):
    recipe_name = State()


@get_recipe_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Без проблем!")
    await message.answer("Итак, что я могу для вас сделать?", reply_markup=menu_keyboard)


@get_recipe_router.message(StateFilter(None), F.text.casefold() == "найти рецепт блюда по названию")
async def get_recipe(message: Message, state: FSMContext):
    await state.set_state(RecipeDatails.recipe_name)
    await message.answer_sticker("CAACAgIAAxkBAAIQq2YVCX2IOu21FjwjlIK_eqU_wnx8AAIwCgAC4_woSqMD6yBTUfobNAQ")
    await message.answer("Введите название блюда", reply_markup=cancel_keyboard)
    
    
@get_recipe_router.message(StateFilter(RecipeDatails.recipe_name), F.text)
async def get_recipe_name(message: Message, state: FSMContext):    
    await message.answer("Начинаю поиск рецепта...")
    gpt_response = generate_response(message.text)
    await message.answer(gpt_response, reply_markup=functional_keyboard)
    await state.clear()
    
    
@get_recipe_router.message(StateFilter(RecipeDatails.recipe_name))
async def incorrect_message(message: Message, state: FSMContext):
    await message.answer("Не понимаю... возможно, вы использовали некорректные данные. Введите название блюда еще раз")
    

@get_recipe_router.message(StateFilter(None), F.text.casefold() == "вернуться к меню")
async def to_menu(message: Message):
    await message.answer("Итак, что я могу для вас сделать?", reply_markup=menu_keyboard)
    
    
@get_recipe_router.message(StateFilter(None), F.text.casefold() == "найти еще рецепт")
async def get_recipe_again(message: Message, state: FSMContext):
    await message.answer("Без проблем!", reply_markup=ReplyKeyboardRemove())
    await get_recipe(message, state)


