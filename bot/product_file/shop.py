from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.product_file.products import get_all_product_data

product_router = Router()
product_list = get_all_product_data()


def product_carousel_keyboard(index: int) -> InlineKeyboardMarkup:
    total = len(product_list)
    prev_index = (index - 1) % total
    next_index = (index + 1) % total

    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="⬅️ Prev", callback_data=f"carousel:{prev_index}"),
        InlineKeyboardButton(text="🛒 Add", callback_data=f"add:{product_list[index]['id']}"),
        InlineKeyboardButton(text="➡️ Next", callback_data=f"carousel:{next_index}")
    )
    return kb.as_markup()


@product_router.message(Command("product"))
async def show_first_product(message: types.Message):
    index = 0
    product = product_list[index]
    text = f"📦 <b>{product['name']}</b>\n💰 <b>Price:</b> ${product['price']}"
    await message.answer(text, reply_markup=product_carousel_keyboard(index), parse_mode='HTML')


@product_router.callback_query(F.data.startswith("carousel:"))
async def handle_carousel(callback: types.CallbackQuery):
    index = int(callback.data.split(":")[1])
    product = product_list[index]
    text = f"📦 <b>{product['name']}</b>\n💰 <b>Price:</b> ${product['price']}"
    await callback.message.edit_text(text, reply_markup=product_carousel_keyboard(index), parse_mode='HTML')
    await callback.answer()
