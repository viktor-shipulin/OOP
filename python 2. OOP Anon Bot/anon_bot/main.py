import os
import sys
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton
)
from anonDB import UserDB

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

try:
    from config import TOKEN, GROUP_ID, ADMIN_ID
except ImportError:
    TOKEN = os.getenv("TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID")
    GROUP_ID = os.getenv("GROUP_ID")
    if ADMIN_ID: ADMIN_ID = int(ADMIN_ID)
    if GROUP_ID: GROUP_ID = int(GROUP_ID)

if not TOKEN:
    sys.exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()
db = UserDB()

class RegStates(StatesGroup):
    waiting_for_nickname = State()

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Новое сообщение")],
            [KeyboardButton(text="ℹ️ Инфо"), KeyboardButton(text="📜 Правила")]
        ],
        resize_keyboard=True
    )

def get_moderation_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_{user_id}")
        ],
        [InlineKeyboardButton(text="🚫 БАН", callback_data=f"banselect_{user_id}")]
    ])

def get_ban_time_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день", callback_data=f"banset_{user_id}_1")],
        [InlineKeyboardButton(text="7 дней", callback_data=f"banset_{user_id}_7")],
        [InlineKeyboardButton(text="30 дней", callback_data=f"banset_{user_id}_30")],
        [InlineKeyboardButton(text="Навсегда", callback_data=f"banset_{user_id}_forever")],
        [InlineKeyboardButton(text="🔙 Отмена", callback_data=f"cancelban_{user_id}")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    ban_status = db.is_banned(message.from_user.id)
    if ban_status:
        await message.answer(f"❌ Доступ закрыт до: {ban_status}")
        return
    if db.is_registered(message.from_user.id):
        await message.answer("✅ Бот готов!", reply_markup=get_main_keyboard())
    else:
        await message.answer("👋 Введи свой псевдоним для регистрации:")
        await state.set_state(RegStates.waiting_for_nickname)

@dp.message(RegStates.waiting_for_nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    db.register(message.from_user.id, message.text)
    await state.clear()
    await message.answer(f"Приятно познакомиться, {message.text}!", reply_markup=get_main_keyboard())

@dp.message(F.chat.type == "private")
async def handle_to_moderator(message: types.Message):
    if message.text in ["ℹ️ Инфо", "📝 Новое сообщение", "📜 Правила"]:
        if message.text == "📜 Правила":
            await message.answer("1. Не спамить.\n2. Минимум 5 символов.\n3. Без мата.")
        elif message.text == "ℹ️ Инфо":
            await message.answer("Анонимный бот для постов в группу.")
        elif message.text == "📝 Новое сообщение":
            await message.answer("✍️ Пришли текст или фото для модерации.")
        return

    ban_status = db.is_banned(message.from_user.id)
    if ban_status or not db.is_registered(message.from_user.id): return

    if message.text and len(message.text) < 5:
        await message.answer("⚠️ Сообщение слишком короткое.")
        return

    try:
        db.log_message(message.from_user.id, message.text if message.text else "[Media]")
        nickname = db.users.get(str(message.from_user.id), "User")
        await bot.send_message(ADMIN_ID, f"🔔 **ПОСТ ОТ: {nickname}** (ID: `{message.from_user.id}`)", parse_mode="Markdown")
        await message.copy_to(chat_id=ADMIN_ID, reply_markup=get_moderation_keyboard(message.from_user.id))
        await message.answer("⏳ Отправлено модератору.")
    except Exception as e:
        logging.error(f"Ошибка отправки админу: {e}")

@dp.callback_query(F.data.startswith("approve_"))
async def approve_handler(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]
    post_num = db.get_next_post_number()
    prefix = f"💎 **Анонимный пост №{post_num}**\n\n"
    try:
        if callback.message.text:
            await bot.send_message(GROUP_ID, f"{prefix}{callback.message.text}", parse_mode="Markdown")
        elif callback.message.photo:
            await bot.send_photo(GROUP_ID, photo=callback.message.photo[-1].file_id, caption=f"{prefix}{callback.message.caption or ''}", parse_mode="Markdown")
        await callback.message.edit_reply_markup(reply_markup=None)
        await bot.send_message(int(user_id), f"✅ Ваш пост опубликован под №{post_num}!")
        await callback.answer("Опубликовано")
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")

@dp.callback_query(F.data.startswith("decline_"))
async def decline_handler(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]
    await callback.message.delete()
    try:
        await bot.send_message(int(user_id), "❌ Ваш пост был отклонен модератором.")
    except: pass
    await callback.answer("Отклонено")

@dp.callback_query(F.data.startswith("banselect_"))
async def ban_select(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=get_ban_time_keyboard(user_id))
    await callback.answer()

@dp.callback_query(F.data.startswith("banset_"))
async def ban_apply(callback: CallbackQuery):
    _, uid, dur = callback.data.split("_")
    days = None if dur == "forever" else int(dur)
    label = "навсегда" if days is None else f"на {days} дн."
    db.add_to_blacklist(uid, days)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"🚫 Пользователь {uid} забанен {label}.")
    try:
        await bot.send_message(int(uid), f"🚫 Ваш доступ ограничен {label}.")
    except: pass
    await callback.answer()

@dp.callback_query(F.data.startswith("cancelban_"))
async def cancel_ban(callback: CallbackQuery):
    uid = callback.data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=get_moderation_keyboard(uid))
    await callback.answer()

async def handle(request):
    return web.Response(text="Bot is alive")

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(dp.start_polling(bot))

async def run_app():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 10000)))
    await start_bot()
    await site.start()
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(run_app())