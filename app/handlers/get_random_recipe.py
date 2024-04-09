from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.keyboards.reply import get_keyboard
from app.handlers.user_private import menu_keyboard
from app.services.gpt_free import generate_response_random

get_random_recipe_router = Router()

functional_keyboard = get_keyboard(
    "Придумать новый рецепт",
    "Вернуться к меню",
    placeholder="Выберите действие", 
    sizes=(2,))

cancel_keyboard = get_keyboard(
    "Отмена",
    placeholder="",
    sizes=(1,)
)

class RandomRecipeDatails(StatesGroup):
    details = State()


@get_random_recipe_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Без проблем!")
    await message.answer("Итак, что я могу для вас сделать?", reply_markup=menu_keyboard)


@get_random_recipe_router.message(StateFilter(None), F.text.casefold() == "подобрать рецепт по предпочтениям")
async def get_recipe(message: Message, state: FSMContext):
    await state.set_state(RandomRecipeDatails.details)
    await message.answer_sticker("CAACAgIAAxkBAAIQq2YVCX2IOu21FjwjlIK_eqU_wnx8AAIwCgAC4_woSqMD6yBTUfobNAQ")
    await message.answer(f"Что вы хотите (например, десерт или суп)? Укажите свои предпочтения\n" +
                         f"Если же вам все равно, то <b>введите ' - '",
                         reply_markup=cancel_keyboard)
    
    
@get_random_recipe_router.message(StateFilter(RandomRecipeDatails.details), F.text)
async def get_recipe_name(message: Message, state: FSMContext):    
    await message.answer("Сейчас что-нибудь придумаю для вас...")
    gpt_response = generate_response_random(message.text)
    
    await message.answer(gpt_response, reply_markup=functional_keyboard)
    await state.clear()
    
    
@get_random_recipe_router.message(StateFilter(RandomRecipeDatails.details))
async def incorrect_message(message: Message, state: FSMContext):
    await message.answer("Не понимаю... возможно, вы использовали некорректные данные. Введите ваши предпочтения еще раз")
    

@get_random_recipe_router.message(StateFilter(None), F.text.casefold() == "вернуться к меню")
async def to_menu(message: Message):
    await message.answer("Итак, что я могу для вас сделать?", reply_markup=menu_keyboard)
    
    
@get_random_recipe_router.message(StateFilter(None), F.text.casefold() == "придумать новый рецепт")
async def get_recipe_again(message: Message, state: FSMContext):
    await message.answer("Без проблем!", reply_markup=ReplyKeyboardRemove())
    await get_recipe(message, state)