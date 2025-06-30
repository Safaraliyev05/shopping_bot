from aiogram import Router
from aiogram.types import CallbackQuery

from bot.category_file.keyboards import build_root_category_keyboard, build_subcategory_keyboard, get_subcategories
from bot.product_file.products import get_products_by_category
from bot.product_file.shop import product_cache, product_carousel_keyboard

category_router = Router()


@category_router.callback_query(lambda c: c.data.startswith("category_"))
async def show_subcategories_or_products(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    subcategories = await get_subcategories(category_id)

    if subcategories:
        keyboard = await build_subcategory_keyboard(category_id)
        await callback.message.edit_caption(
            caption="Iltimos, subkategoriyani tanlang:",
            reply_markup=keyboard
        )
    else:
        product_list = await get_products_by_category(category_id)
        if not product_list:
            await callback.answer("Bu kategoriyada mahsulotlar yo‘q.", show_alert=True)
            return

        product_cache[category_id] = product_list
        product = product_list[0]
        text = f"📦 <b>{product['name']}</b>\n💰 <b>Narx:</b> ${product['price']}"
        await callback.message.edit_caption(
            caption=text,
            reply_markup=product_carousel_keyboard(category_id, 0),
            parse_mode='HTML'
        )
        await callback.answer()


@category_router.callback_query(lambda c: c.data == "back_to_root")
async def back_to_categories(callback: CallbackQuery):
    keyboard = await build_root_category_keyboard()
    await callback.message.edit_caption(
        "Kategoriya tanlang:",
        reply_markup=keyboard
    )
