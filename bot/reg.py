import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.category_file.category import category_router
from bot.category_file.keyboards import build_root_category_keyboard

TOKEN = "7063469997:AAEziSALHUctBBljOLdNYQiQw2Y67bYQWws"
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(category_router)


class Register(StatesGroup):
    language = State()
    full_name = State()
    phone_number = State()


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O‘zbekcha"), KeyboardButton(text="🇷🇺 Русский")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Tilni tanlang / Выберите язык:", reply_markup=keyboard)
    await state.set_state(Register.language)


@dp.message(Register.language)
async def choose_language(message: Message, state: FSMContext):
    lang = message.text
    if "O‘zbekcha" in lang:
        await state.update_data(language="uz")
        await message.answer("Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    elif "Русский" in lang:
        await state.update_data(language="ru")
        await message.answer("Введите ваше имя:", reply_markup=ReplyKeyboardRemove())
    else:
        return await message.answer(
            "Iltimos, tilni tugmalar orqali tanlang / Пожалуйста, выберите язык с помощью кнопок.")

    await state.set_state(Register.full_name)


@dp.message(Register.full_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    lang = data.get("language", "uz")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish / Отправить номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    if lang == "uz":
        await message.answer("Telefon raqamingizni yuboring:", reply_markup=keyboard)
    else:
        await message.answer("Отправьте свой номер телефона:", reply_markup=keyboard)

    await state.set_state(Register.phone_number)


@dp.message(Register.phone_number, F.contact)
async def process_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = data["full_name"]
    phone = message.contact.phone_number
    lang = data.get("language", "uz")

    await state.update_data(phone_number=phone)

    keyboard = await build_root_category_keyboard()

    if lang == "uz":
        await message.answer_photo(
            photo="https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
            caption="Iltimos, kategoriyani tanlang:",
            reply_markup=keyboard,
        )
    else:
        await message.answer_photo(
            photo="https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
            caption="Пожалуйста, выберите категорию:",
            reply_markup=keyboard,
        )

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
