import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.api import create_user

TOKEN = "7063469997:AAEziSALHUctBBljOLdNYQiQw2Y67bYQWws"

bot = Bot(TOKEN)
dp = Dispatcher()


class Register(StatesGroup):
    full_name = State()
    phone_number = State()


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Register.full_name)


@dp.message(Register.full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    contact_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=contact_button)
    await state.set_state(Register.phone_number)


@dp.message(Register.phone_number, F.contact)
async def get_phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = data["full_name"]
    phone_number = message.contact.phone_number

    response = create_user(full_name, phone_number)

    if response.status_code == 201:
        await message.answer("Muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=None)
    else:
        await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.", reply_markup=None)

    await state.clear()


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
