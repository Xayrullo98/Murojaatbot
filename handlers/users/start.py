from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu import menu_buttons, phone_buttons, confirm_buttons
from states.appeal import AppealState
from loader import dp, bot, base


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}! botga hush kelibsiz",
                         reply_markup=menu_buttons)


@dp.message_handler(text="Murojaat yuborish")
async def bot_start(message: types.Message):
    await message.answer(f"Ismingizni kiriting...",
                         reply_markup=types.ReplyKeyboardRemove())
    await AppealState.name.set()


@dp.message_handler(state=AppealState.name)
async def bot_start(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data({"name": text})
    await message.answer(f"Familyangizni kiriting...",
                         reply_markup=types.ReplyKeyboardRemove())
    await AppealState.last_name.set()


@dp.message_handler(state=AppealState.last_name)
async def bot_start(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data({"last_name": text})
    await message.answer(f"Telefon raqamingizni kiriting...",
                         reply_markup=phone_buttons)
    await AppealState.phone.set()


@dp.message_handler(state=AppealState.phone, content_types=types.ContentTypes.CONTACT)
async def bot_start(message: types.Message, state: FSMContext):
    text = message.contact.phone_number
    await state.update_data({"phone": text})
    await message.answer(f"Murojaatingizni kiriting...",
                         reply_markup=types.ReplyKeyboardRemove())
    await AppealState.appeal.set()


@dp.message_handler(state=AppealState.phone)
async def bot_start(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) < 9 or len(text) > 13:
        await message.answer(text="No'merni faqat (XXYYYYYYY)da kiriting")
        await AppealState.phone.set()

    elif '93' in text \
            or '94' in text \
            or "90" in text \
            or "91" in text \
            or "33" in text \
            or "88" in text \
            or "95" in text \
            or "97" in text \
            or "98" in text \
            or "99" in text \
            or "71" in text \
            or "50" in text \
            or "20" in text \
            or "78" in text:
        await state.update_data({"phone": text})
        await message.answer(f"Murojaatingizni kiriting...",
                             reply_markup=types.ReplyKeyboardRemove())
        await AppealState.appeal.set()
    else:
        await message.answer(text="No'merni faqat (XXYYYYYYY)da kiriting")
        await AppealState.phone.set()


@dp.message_handler(state=AppealState.appeal)
async def bot_start(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data({"appeal": text})
    data = await state.get_data()
    name = data.get('name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    appeal = data.get('appeal')
    await bot.send_message(chat_id=message.from_user.id, text=f"{name} {last_name} \n"
                                                              f"{appeal}\n"
                                                              f"📞 <a href='tel:{phone}' >{phone}</a>",
                           reply_markup=confirm_buttons)
    await AppealState.confirm.set()


@dp.message_handler(state=AppealState.confirm, text="Tasdiqlash")
async def bot_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    appeal = data.get('appeal')
    admins = base.select_all_admins()
    for admin in admins:
        try:
            await bot.send_message(chat_id=admin[1], text=f"{name} {last_name} \n"
                                                      f"{appeal}\n"
                                                      f"📞 <a href='tel:{phone}' >{phone}</a>",
                               reply_markup=menu_buttons)
        except Exception as x:
            await bot.send_message(chat_id='6570924683',text=f"{x}")
    await bot.send_message(chat_id=message.from_user.id, text="Adminga yuborildi", reply_markup=menu_buttons)
    await state.finish()


@dp.message_handler(state=AppealState.confirm, text="Bekor qilish")
async def bot_start(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text="Bekor qilindi", reply_markup=menu_buttons)
    await state.finish()
