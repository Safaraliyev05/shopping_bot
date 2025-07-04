from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.category_file.keyboards import build_subcategory_keyboard, get_parent_id_of_category, \
    build_root_category_keyboard
from bot.product_file.products import get_products_by_category

product_router = Router()
product_cache = {}


def product_carousel_keyboard(subcat_id: int, index: int) -> InlineKeyboardMarkup:
    product_list = product_cache.get(subcat_id, [])
    total = len(product_list)
    prev_index = (index - 1) % total
    next_index = (index + 1) % total

    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="⬅️ Prev", callback_data=f"carousel:{subcat_id}:{prev_index}"),
        InlineKeyboardButton(text="🛒 Add", callback_data=f"add:{product_list[index]['id']}"),
        InlineKeyboardButton(text="➡️ Next", callback_data=f"carousel:{subcat_id}:{next_index}")
    )
    kb.row(
        InlineKeyboardButton(text="🔙 Ortga", callback_data=f"back_to_subcategory:{subcat_id}")
    )
    return kb.as_markup()


@product_router.callback_query(F.data.startswith("subcategory_"))
async def show_products_for_subcategory(callback: types.CallbackQuery):
    subcat_id = int(callback.data.split("_")[1])
    product_list = await get_products_by_category(subcat_id)

    if not product_list:
        await callback.answer("Bu kategoriyada mahsulotlar yo'q.", show_alert=True)
        return

    product_cache[subcat_id] = product_list
    product = product_list[0]
    text = f"📦 <b>{product['name']}</b>\n💰 <b>Narx:</b> ${product['price']}"
    await callback.message.edit_caption(
        caption=text,
        reply_markup=product_carousel_keyboard(subcat_id, 0),
        parse_mode='HTML'
    )
    await callback.answer()


@product_router.callback_query(F.data.startswith("carousel:"))
async def handle_carousel(callback: types.CallbackQuery):
    try:
        _, subcat_id, index = callback.data.split(":")
        subcat_id = int(subcat_id)
        index = int(index)
    except (ValueError, IndexError):
        return await callback.answer("Xatolik yuz berdi.")

    product_list = product_cache.get(subcat_id, [])

    if not product_list:
        await callback.answer("Mahsulotlar topilmadi.", show_alert=True)
        return

    product = product_list[index]
    text = f"📦 <b>{product['name']}</b>\n💰 <b>Narx:</b> ${product['price']}"
    await callback.message.edit_caption(
        caption=text,
        reply_markup=product_carousel_keyboard(subcat_id, index),
        parse_mode='HTML'
    )
    await callback.answer()


@product_router.callback_query(F.data.startswith("back_to_subcategory:"))
async def back_to_subcategory(callback: CallbackQuery):
    try:
        subcat_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        return await callback.answer("Xatolik yuz berdi.")

    parent_id = await get_parent_id_of_category(subcat_id)

    if parent_id is None:
        keyboard = await build_root_category_keyboard()
        await callback.message.edit_caption(
            caption="Kategoriya tanlang:",
            reply_markup=keyboard,
        )
        return

    keyboard = await build_subcategory_keyboard(parent_id)
    await callback.message.edit_caption(
        caption="Iltimos, subkategoriyani tanlang:",
        reply_markup=keyboard,
    )
    await callback.answer()
