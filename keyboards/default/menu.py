from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from loader import base

menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Murojaat yuborish")
        ]
    ],
    resize_keyboard=True
)
admin_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Admin qo'shish"),
            KeyboardButton(text="Admin o'chirish"),
        ]
    ],
    resize_keyboard=True
)

phone_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kantakt yuborish", request_contact=True),

        ]
    ],
    resize_keyboard=True
)

confirm_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tasdiqlash"),
            KeyboardButton(text="Bekor qilish"),
        ]
    ],
    resize_keyboard=True
)


async def admins_list():
    car_models = base.select_all_admins()
    index = 0
    keys = []
    j = 0
    for model in car_models:
            keys.append(InlineKeyboardButton(text=f'{model[2]}',callback_data=f"{model[0]}"))

    # keys.append([KeyboardButton(text="Ortga")])
    course_buttons = InlineKeyboardMarkup(inline_keyboard=[keys],row_width=1)
    return course_buttons
