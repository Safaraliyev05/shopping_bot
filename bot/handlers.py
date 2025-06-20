import os
import django

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")  # replace with your project name
django.setup()

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from .menu_processing import get_product_data

test = Router()


@test.message(Command("products"))
async def show_products(message: Message):
    image_path, caption, keyboard = await get_product_data(page=1)

    if not image_path:
        await message.answer("Mahsulot topilmadi.")
        return

    photo = FSInputFile(image_path)
    await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard)


@test.callback_query(F.data.startswith("2|"))
async def paginate_products(callback: CallbackQuery):
    _, direction, category_id, page = callback.data.split("|")
    page = int(page)

    image_path, caption, keyboard = await get_product_data(page=page, category_id=int(category_id))

    if not image_path:
        await callback.answer("Mahsulot yo‘q")
        return

    media = FSInputFile(image_path)
    await callback.message.edit_media(
        media=InputMediaPhoto(media=media, caption=caption),
        reply_markup=keyboard,
    )
