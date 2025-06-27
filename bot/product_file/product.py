from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

product_router = Router()


@product_router.message(Command("product"))
async def start(message: Message):
    a = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ortga", callback_data="pre_product"),
             InlineKeyboardButton(text="Product number", callback_data="product_number"),
             InlineKeyboardButton(text="Keyingi", callback_data="next_product"), ],
            [InlineKeyboardButton(text="🛒Korzinka", callback_data="korzinka"), ],
        ]
    )
    await message.answer('Products', caption="Kategoriya tanlang", reply_markup=a)
