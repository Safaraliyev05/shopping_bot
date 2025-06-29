import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")  # change as needed
django.setup()
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from apps.models import Category


@sync_to_async
def get_root_categories():
    return list(Category.objects.filter(parent__isnull=True))


@sync_to_async
def get_subcategories(parent_id):
    return list(Category.objects.filter(parent_id=parent_id))


async def build_root_category_keyboard():
    categories = await get_root_categories()
    inline_keyboard = []

    for cat in categories:
        inline_keyboard.append([
            InlineKeyboardButton(
                text=cat.name_uz,
                callback_data=f"category_{cat.id}",
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def build_subcategory_keyboard(parent_id):
    subcategories = await get_subcategories(parent_id)
    inline_keyboard = []

    for subcat in subcategories:
        inline_keyboard.append([
            InlineKeyboardButton(
                text=subcat.name_uz,
                callback_data=f"category_{subcat.id}",
            )
        ])

    inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_to_root")
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
