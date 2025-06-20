# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
#
# product_router = Router()
# test = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="Ortga", callback_data="previous"),
#          InlineKeyboardButton(text="Product Number", callback_data="next"),
#          InlineKeyboardButton(text="Keyingi", callback_data="next")],
#         [InlineKeyboardButton(text="🛒", callback_data="sport"),
#          InlineKeyboardButton(text="Ortga", callback_data="sport")],
#     ]
# )
#
#
# @product_router.message(Command("test"))
# async def start(message: Message):
#     media = "photo of product"
#     await message.answer_photo(media, caption="Name of product", reply_markup=test)


# import os
# import django
#
# # Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")  # replace with your project name
# django.setup()
#
# from aiogram import Router, F
# from aiogram.filters import Command
# from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
# from asgiref.sync import sync_to_async
#
# from apps.models import Product, ProductColor, ProductImage, User, Cart, CartItem  # replace with your app name
#
# product_router = Router()
#
#
# def generate_product_keyboard(product_id: int) -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="🛒 Savatga qo‘shish", callback_data=f"add_to_cart:{product_id}")],
#             [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back")]
#         ]
#     )
#
#
# @product_router.message(Command("test"))
# async def show_product(message: Message):
#     # Use sync_to_async to call Django ORM
#     product = await sync_to_async(lambda: Product.objects.prefetch_related('images', 'colors').first())()
#
#     if not product:
#         await message.answer("Hozircha hech qanday mahsulot mavjud emas.")
#         return
#
#     # Fetch image and color
#     image = await sync_to_async(lambda: product.images.first())()
#     color = await sync_to_async(lambda: product.colors.first())()
#
#     caption = f"🛍 <b>{product.name_uz}</b>\n"
#     if color:
#         caption += f"💵 Narxi: {color.price} so‘m\n"
#
#     if image and os.path.exists(image.image.path):
#         photo = FSInputFile(image.image.path)
#         await message.answer_photo(
#             photo=photo,
#             caption=caption,
#             reply_markup=generate_product_keyboard(product.id),
#             parse_mode="HTML"
#         )
#     else:
#         await message.answer(
#             caption,
#             reply_markup=generate_product_keyboard(product.id),
#             parse_mode="HTML"
#         )
#
#
# @product_router.callback_query(F.data.startswith("add_to_cart:"))
# async def add_to_cart(callback: CallbackQuery):
#     product_id = int(callback.data.split(":")[1])
#     tg_user = callback.from_user
#
#     # Ensure user exists
#     user, _ = await sync_to_async(User.objects.get_or_create)(
#         full_name=tg_user.full_name or "No Name",
#         phone_number=""
#     )
#
#     cart, _ = await sync_to_async(Cart.objects.get_or_create)(user=user)
#
#     product_color = await sync_to_async(lambda: ProductColor.objects.filter(product_id=product_id).first())()
#     if not product_color:
#         await callback.answer("Mahsulot rangi topilmadi.", show_alert=True)
#         return
#
#     # Add or update CartItem
#     def get_or_create_cart_item():
#         item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             product_color=product_color,
#             defaults={"quantity": 1}
#         )
#         if not created:
#             item.quantity += 1
#             item.save()
#         return item
#
#     await sync_to_async(get_or_create_cart_item)()
#
#     await callback.answer("🛒 Mahsulot savatga qo‘shildi!", show_alert=True)
import os

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")  # change as needed
django.setup()

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from asgiref.sync import sync_to_async
from apps.models import Product  # change as needed

product_router = Router()
PRODUCTS_PER_PAGE = 1


def generate_product_keyboard(page: int, product_id: int, total: int) -> InlineKeyboardMarkup:
    buttons = []

    # Pagination buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Ortga", callback_data=f"show_product:{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(text=f"📦 {page}/{total}", callback_data="ignore"))
    if page < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"show_product:{page + 1}"))
    buttons.append(nav_buttons)

    # Cart button
    buttons.append([
        InlineKeyboardButton(text="🛒 Savatga qo‘shish", callback_data=f"add_to_cart:{product_id}")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# /test starts from page 1
@product_router.message(Command("test"))
async def show_first_product(message: Message):
    await show_product_page(message=message, callback=None, page=1)


# Callback for any page
@product_router.callback_query(F.data.startswith("show_product:"))
async def handle_product_page(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await show_product_page(message=None, callback=callback, page=page)


# Reusable product display function
from aiogram.types import InputMediaPhoto


async def show_product_page(message: Message = None, callback: CallbackQuery = None, page: int = 1):
    products = await sync_to_async(list)(Product.objects.all().prefetch_related('images', 'colors'))
    total = len(products)

    if total == 0 or page > total or page < 1:
        msg = "Mahsulot topilmadi."
        if message:
            await message.answer(msg)
        elif callback:
            await callback.message.edit_text(msg)
        return

    product = products[page - 1]
    image = await sync_to_async(lambda: product.images.first())()
    color = await sync_to_async(lambda: product.colors.first())()

    caption = f"🛍 <b>{product.name_uz}</b>\n"
    if color:
        caption += f"💵 Narxi: {color.price} so‘m\n"

    keyboard = generate_product_keyboard(page=page, product_id=product.id, total=total)

    if image and os.path.exists(image.image.path):
        if message:
            # First-time message
            photo = FSInputFile(image.image.path)
            await message.answer_photo(photo, caption=caption, reply_markup=keyboard, parse_mode="HTML")
        elif callback:
            # Update photo using InputMediaPhoto (required)
            media = InputMediaPhoto(
                media=FSInputFile(image.image.path),
                caption=caption,
                parse_mode="HTML"
            )
            await callback.message.edit_media(media=media, reply_markup=keyboard)
    else:
        # No image: just text
        if message:
            await message.answer(caption, reply_markup=keyboard, parse_mode="HTML")
        elif callback:
            await callback.message.edit_text(caption, reply_markup=keyboard, parse_mode="HTML")


# Prevent clicking disabled center button
@product_router.callback_query(F.data == "ignore")
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()
