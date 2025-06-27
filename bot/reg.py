import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.category_file.category import router
from bot.category_file.keyboards import category_keyboard
from bot.product_file.product import product_router

TOKEN = "7063469997:AAEziSALHUctBBljOLdNYQiQw2Y67bYQWws"
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.include_router(product_router    )


class Register(StatesGroup):
    language = State()
    full_name = State()
    phone_number = State()
    shop_category = State()


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

    if lang == "uz":
        await message.answer("Kategoriyani tanlang:", reply_markup=category_keyboard)
    else:
        await message.answer("Выберите категорию:", reply_markup=category_keyboard)

    await state.set_state(Register.shop_category)


@dp.message(Register.shop_category, F.text)
async def process_shop_category(message: Message, state: FSMContext):
    selected = message.text
    data = await state.get_data()
    lang = data.get("language", "uz")

    await state.update_data(shop_category=selected)

    if lang == "uz":
        await message.answer(f"{selected} kategoriyasi tanlandi. Ro'yxat yakunlandi ✅",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Вы выбрали категорию: {selected}. Регистрация завершена ✅",
                             reply_markup=ReplyKeyboardRemove())

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
