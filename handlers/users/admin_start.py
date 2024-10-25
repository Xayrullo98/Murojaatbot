from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.config import ADMINS
from keyboards.default.menu import admin_buttons, admins_list
from loader import dp, base, bot
from states.appeal import AdminState


@dp.message_handler(CommandStart(), chat_id=[admin for admin in ADMINS])
async def bot_echo(message: types.Message):
    await message.answer(text="botga xush kelibsiz", reply_markup=admin_buttons)


@dp.message_handler(text="Admin qo'shish", chat_id=[admin for admin in ADMINS])
async def bot_echo(message: types.Message):
    await message.answer(text="Admin ismini kiriting", reply_markup=types.ReplyKeyboardRemove())
    await AdminState.name.set()


@dp.message_handler(state=AdminState.name, chat_id=[admin for admin in ADMINS])
async def bot_echo(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer(text="Admin tg_idsini kiriting", reply_markup=types.ReplyKeyboardRemove())
    await AdminState.tg_id.set()


@dp.message_handler(state=AdminState.tg_id, chat_id=[admin for admin in ADMINS])
async def bot_echo(message: types.Message, state: FSMContext):
    text = message.text
    if text.isdigit():
        await state.update_data({"tg_id": text})
        data = await state.get_data()
        base.add_admin(name=data.get('name'), tg_id=data.get('tg_id'))
        await message.answer(text="Admin qo'shildi", reply_markup=admin_buttons)
        await state.finish()
    else:
        await message.answer(text=" tg_idni faqat sonda kiriting", reply_markup=types.ReplyKeyboardRemove())
        await AdminState.tg_id.set()


@dp.message_handler(text="Admin o'chirish", chat_id=[admin for admin in ADMINS])
async def bot_echo(message: types.Message):
    admin_buttons = await admins_list()
    await message.answer(text="O'chirmoqchi bo'lgan adminni tanlang", reply_markup=admin_buttons)
@dp.callback_query_handler()
async def bot_echo(message: types.CallbackQuery):
    data = message.data
    base.delete_admin(id=int(data))
    admin_buttons = await admins_list()
    await bot.edit_message_reply_markup(chat_id=message.from_user.id,message_id=message.message.message_id, reply_markup=admin_buttons)