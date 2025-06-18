from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile

from bot.category_file.keyboards import category_keyboard, elektronika_keyboard, kiyim_keyboard, sport_keyboard

router = Router()


@router.message(Command("shop"))
async def start(message: Message):
    media = FSInputFile("elek.jpg")
    await message.answer_photo(photo=media, caption="Kategoriya tanlang", reply_markup=category_keyboard)


@router.callback_query()
async def callback_query(callback: CallbackQuery):
    data = callback.data

    if data == "elektronika":
        media = InputMediaPhoto(
            media=FSInputFile("elek.jpg"),
            caption="Elektronika\nIltimos categoriyani tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=elektronika_keyboard)

    elif data == "kiyim":
        media = InputMediaPhoto(
            media=FSInputFile("elek.jpg"),
            caption="Kiyim\nIltimos categoriyani tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=kiyim_keyboard)

    elif data == "sport":
        media = InputMediaPhoto(
            media=FSInputFile("elek.jpg"),
            caption="Sport\nIltimos categoriyani tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=sport_keyboard)

    elif data == "back_category":
        media = InputMediaPhoto(
            media=FSInputFile("elek.jpg"),
            caption="Kategoriya tanlang",
        )
        await callback.message.edit_media(media=media, reply_markup=category_keyboard)
