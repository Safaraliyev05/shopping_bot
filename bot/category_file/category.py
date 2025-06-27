from aiogram import Router
from aiogram.types import CallbackQuery, InputMediaPhoto

from bot.category_file.keyboards import category_keyboard, elektronika_keyboard, kiyim_keyboard, sport_keyboard

router = Router()


@router.callback_query()
async def callback_query(callback: CallbackQuery):
    data = callback.data

    if data == "elektronika":
        media = InputMediaPhoto(
            media="https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
            caption="Elektronika\nIltimos categoriyani tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=elektronika_keyboard)

    elif data == "kiyim":
        media = InputMediaPhoto(
            media="https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
            caption="Kiyim\nIltimos categoriyani tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=kiyim_keyboard)

    elif data == "sport":
        media = InputMediaPhoto(
            media="https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
            caption="Sport\nIltimos categoriyani tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=sport_keyboard)

    elif data == "back_category":
        media = InputMediaPhoto(
            media="https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
            caption="Kategoriya tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=category_keyboard)
