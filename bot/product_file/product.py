# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
#
# product_router = Router()
#
#
# @product_router.message(Command("product"))
# async def start(message: Message):
#     a = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="Ortga", callback_data="pre_product"),
#              InlineKeyboardButton(text="Product number", callback_data="product_number"),
#              InlineKeyboardButton(text="Keyingi", callback_data="next_product"), ],
#             [InlineKeyboardButton(text="🛒Korzinka", callback_data="korzinka"), ],
#         ]
#     )
#     await message.answer('Products', caption="Kategoriya tanlang", reply_markup=a)
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")  # change as needed
django.setup()
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator

from apps.models import Product

product_router = Router()
PRODUCTS_PER_PAGE = 1  # One product at a time


# ====== UTILS ======
@sync_to_async
def get_products_by_category(category_id=None):
    qs = Product.objects.prefetch_related('images', 'colors')
    if category_id:
        qs = qs.filter(categories__id=category_id)
    return list(qs)


def get_products_btns(level, category, page, pagination_btns, product_id):
    buttons = []

    # First row: pagination
    pagination_row = []
    if pagination_btns.get("◀ Пред."):
        pagination_row.append(InlineKeyboardButton(
            text="◀ Пред.", callback_data=pagination_btns["◀ Пред."]
        ))
    else:
        pagination_row.append(InlineKeyboardButton(text=" ", callback_data="noop"))

    pagination_row.append(InlineKeyboardButton(
        text=f"{page}", callback_data="noop"
    ))

    if pagination_btns.get("След. ▶"):
        pagination_row.append(InlineKeyboardButton(
            text="След. ▶", callback_data=pagination_btns["След. ▶"]
        ))
    else:
        pagination_row.append(InlineKeyboardButton(text=" ", callback_data="noop"))

    buttons.append(pagination_row)

    # Second row: Cart button
    buttons.append([
        InlineKeyboardButton(text="🛒 В корзину", callback_data=f"add_to_cart_{product_id}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def show_product(message_or_callback, level, category, page):
    products = await get_products_by_category(category_id=category)

    if not products:
        raise ValueError("No products found for the selected category.")

    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]

    colors = await sync_to_async(list)(product.colors.all())
    color_text = "\n".join([f"{c.color_name} - {c.price} so'm" for c in colors]) or "Ranglar yo'q"

    caption = (
        f"<strong>{product.name_uz}</strong>\n\n"
        f"{color_text}\n\n"
        f"<strong>Товар {paginator.page} из {paginator.pages}</strong>"
    )

    images = await sync_to_async(list)(product.images.all())
    if images:
        photo_url = f"/media/{images[0].image}"
    else:
        photo_url = "https://via.placeholder.com/300"

    image = InputMediaPhoto(media=photo_url, caption=caption, parse_mode="HTML")

    pagination_btns = {}
    if paginator.has_previous():
        pagination_btns["◀ Пред."] = f"product_page_{paginator.page-1}"
    if paginator.has_next():
        pagination_btns["След. ▶"] = f"product_page_{paginator.page+1}"

    kbds = get_products_btns(
        level=level,
        category=category,
        page=paginator.page,
        pagination_btns=pagination_btns,
        product_id=product.id,
    )

    if isinstance(message_or_callback, Message):
        await message_or_callback.answer_photo(
            photo=photo_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=kbds
        )
    elif isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_media(
            media=image,
            reply_markup=kbds
        )


# ====== ROUTES ======
@product_router.message(Command("product"))
async def cmd_product(message: Message):
    await show_product(message, level=0, category=None, page=1)


@product_router.callback_query(lambda c: c.data.startswith("product_page_"))
async def cb_paginate(callback: CallbackQuery):
    try:
        page = int(callback.data.split("_")[-1])
    except ValueError:
        await callback.answer("Неверный номер страницы.")
        return

    await show_product(callback, level=0, category=None, page=page)


@product_router.callback_query(lambda c: c.data.startswith("add_to_cart_"))
async def cb_add_to_cart(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split("_")[-1])
    except ValueError:
        await callback.answer("Некорректный товар.")
        return

    # OPTIONAL: Add your cart logic here
    # await add_to_cart(user_id=callback.from_user.id, product_id=product_id)
    logging.info(f"User {callback.from_user.id} added product {product_id} to cart.")

    await callback.answer("✅ Товар добавлен в корзину!")
