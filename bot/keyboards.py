from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()
builder.row(types.InlineKeyboardButton(text="200 $", url="https://uzum.uz/uz/product/universal-kostyum-ikki-784245"))
builder.row(types.InlineKeyboardButton(text="Axaxa", url="https://uzum.uz/uz/product/universal-kostyum-ikki-784245"))

category_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Elektronika')],
        [KeyboardButton(text='Maishiy Texnika')],
        [KeyboardButton(text='Kiyim')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
