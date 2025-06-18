from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Elektronika", callback_data="elektronika")],
        [InlineKeyboardButton(text="Kiyim", callback_data="kiyim")],
        [InlineKeyboardButton(text="Sport va hobbiy", callback_data="sport")],
    ]
)

elektronika_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Telefon", callback_data="telefon"),
         InlineKeyboardButton(text="Kompyuter", callback_data="kompyuter")],
        [InlineKeyboardButton(text="Noutbuk", callback_data="noutbuk"),
         InlineKeyboardButton(text="Ortga", callback_data="back_category")],
    ]
)

kiyim_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Erkaklar kiyimi", callback_data="erkak_kiyim"),
         InlineKeyboardButton(text="Ayollar kiyimi", callback_data="ayol_kiyim")],
        [InlineKeyboardButton(text="Bolalar kiyimi", callback_data="bola_kiiyim"),
         InlineKeyboardButton(text="Ortga", callback_data="back_category")],
    ]
)

sport_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Fudbol", callback_data="fudbol"),
         InlineKeyboardButton(text="Basketbol", callback_data="basketbol")],
        [InlineKeyboardButton(text="Voleybol", callback_data="voleybol"),
         InlineKeyboardButton(text="Ortga", callback_data="back_category")],
    ]
)
