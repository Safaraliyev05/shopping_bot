from aiogram import Router
from aiogram.types import CallbackQuery

from bot.category_file.keyboards import build_root_category_keyboard, build_subcategory_keyboard

category_router = Router()


@category_router.callback_query(lambda c: c.data.startswith("category_"))
async def show_subcategories(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    keyboard = await build_subcategory_keyboard(category_id)
    await callback.message.edit_caption(
        "Iltimos, subkategoriyani tanlang:",
        reply_markup=keyboard
    )


@category_router.callback_query(lambda c: c.data == "back_to_root")
async def back_to_categories(callback: CallbackQuery):
    keyboard = await build_root_category_keyboard()
    await callback.message.edit_caption(
        "Kategoriya tanlang:",
        reply_markup=keyboard
    )
