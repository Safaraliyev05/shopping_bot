from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

product_router = Router()
test = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ortga", callback_data="previous"),
         InlineKeyboardButton(text="Mahsulot raqami", callback_data="next"),
         InlineKeyboardButton(text="Keyingi", callback_data="next")],
        [InlineKeyboardButton(text="Korzinka", callback_data="sport"),
         InlineKeyboardButton(text="Ortga", callback_data="sport")],
    ]
)


@product_router.message(Command("test"))
async def start(message: Message):
    await message.answer("Mahsulot", reply_markup=test)
