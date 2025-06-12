import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

from apps.models import User

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = "7063469997:AAEziSALHUctBBljOLdNYQiQw2Y67bYQWws"
bot = Bot(token=TOKEN)
dp = Dispatcher()


class Register(StatesGroup):
    full_name = State()
    phone_number = State()


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Register.full_name)


@dp.message(Register.full_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=keyboard)
    await state.set_state(Register.phone_number)


@dp.message(Register.phone_number, F.contact)
async def process_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = data["full_name"]
    phone = message.contact.phone_number

    User.objects.create(full_name=full_name, phone_number=phone)

    await message.answer("Ro'yxatdan o'tdingiz!")
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
