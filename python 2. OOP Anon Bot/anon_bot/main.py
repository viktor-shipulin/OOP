# main.py
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton
)

from config import TOKEN, GROUP_ID, ADMIN_ID
from anonDB import UserDB

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

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
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"approve_{user_id}"),
             InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_{user_id}")],
            [InlineKeyboardButton(text="🚫 БАН", callback_data=f"banselect_{user_id}")]
        ]
    )


def get_ban_time_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 день", callback_data=f"banset_{user_id}_1")],
            [InlineKeyboardButton(text="7 дней", callback_data=f"banset_{user_id}_7")],
            [InlineKeyboardButton(text="Навсегда", callback_data=f"banset_{user_id}_forever")],
            [InlineKeyboardButton(text="🔙 Отмена", callback_data=f"cancelban_{user_id}")]
        ]
    )


async def check_admin(callback: CallbackQuery) -> bool:
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет прав администратора", show_alert=True)
        return False
    return True


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    ban_status = db.is_banned(message.from_user.id)
    if ban_status:
        await message.answer(f"❌ Доступ закрыт до: {ban_status}")
        return

    if db.is_registered(message.from_user.id):
        await message.answer("✅ Бот готов к работе!", reply_markup=get_main_keyboard())
    else:
        await message.answer("👋 Привет! Введи свой псевдоним (никнейм):")
        await state.set_state(RegStates.waiting_for_nickname)


@dp.message(Command("unban"))
async def cmd_unban(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.answer("Использование: /unban <user_id>")
        return
    
    user_id = args[1]
    if db.remove_from_blacklist(user_id):
        await message.answer(f"✅ Пользователь {user_id} разбанен")
    else:
        await message.answer("❌ Пользователь не найден в бане")


@dp.message(Command("banlist"))
async def cmd_banlist(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    ban_list = db.get_ban_list()
    if not ban_list:
        await message.answer("📭 Чёрный список пуст")
    else:
        text = "🚫 **Забаненные пользователи:**\n\n" + "\n".join(ban_list)
        await message.answer(text)


@dp.message(RegStates.waiting_for_nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    nickname = message.text.strip()
    if len(nickname) < 2:
        await message.answer("❌ Имя должно быть не короче 2 символов. Попробуй снова:")
        return
    
    db.register(message.from_user.id, nickname)
    await state.clear()
    await message.answer(
        f"✅ Регистрация завершена!\nПриятно познакомиться, {nickname}!",
        reply_markup=get_main_keyboard()
    )


@dp.message(F.chat.type == "private")
async def handle_private(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == RegStates.waiting_for_nickname.state:
        return  

    ban_status = db.is_banned(message.from_user.id)
    if ban_status:
        await message.answer(f"❌ Вы забанены. Срок: {ban_status}")
        return

    if not db.is_registered(message.from_user.id):
        await message.answer("❌ Сначала зарегистрируйся через /start")
        return

    if message.text in ["📝 Новое сообщение", "ℹ️ Инфо", "📜 Правила"]:
        if message.text == "📜 Правила":
            await message.answer(
                "📜 **Правила чата:**\n\n"
                "1. Не спамить\n"
                "2. Минимум 5 символов в сообщении\n"
                "3. Запрещён мат и оскорбления\n"
                "4. Только по теме"
            )
        elif message.text == "ℹ️ Инфо":
            await message.answer(
                "ℹ️ **О боте:**\n\n"
                "Это анонимный бот для отправки сообщений в группу.\n"
                "Все сообщения проходят модерацию."
            )
        elif message.text == "📝 Новое сообщение":
            await message.answer("✍️ Отправь текст, фото или видео для публикации:")
        return

    if message.text and len(message.text) < 3:
        await message.answer("❌ Сообщение слишком короткое (минимум 3 символа)")
        return

    content_type = "📝 Текст" if message.text else "🖼 Медиа"
    db.log_message(message.from_user.id, f"[{content_type}] {message.text if message.text else ''}")
    
    nickname = db.users.get(str(message.from_user.id), "Пользователь")

    try:
        await bot.send_message(
            ADMIN_ID,
            f"🔔 **Новый пост на модерацию**\n"
            f"👤 От: {nickname}\n"
            f"🆔 ID: `{message.from_user.id}`"
        )
        
        await message.copy_to(
            chat_id=ADMIN_ID,
            reply_markup=get_moderation_keyboard(message.from_user.id)
        )
        
        await message.answer("⏳ Сообщение отправлено на модерацию")
        
    except Exception as e:
        logging.error(f"Ошибка отправки админу: {e}")
        await message.answer("❌ Произошла ошибка при отправке")


@dp.callback_query(F.data.startswith("approve_"))
async def approve_handler(callback: CallbackQuery):
    if not await check_admin(callback):
        return

    user_id = int(callback.data.split("_")[1])
    post_num = db.get_next_post_number()
    msg = callback.message

    prefix = f"💎 **Анонимный пост №{post_num}**\n\n"

    try:
        if msg.text:
            await bot.send_message(GROUP_ID, f"{prefix}{msg.text}")
        elif msg.photo:
            await bot.send_photo(
                GROUP_ID,
                photo=msg.photo[-1].file_id,
                caption=prefix + (msg.caption or "")
            )
        elif msg.video:
            await bot.send_video(
                GROUP_ID,
                video=msg.video.file_id,
                caption=prefix + (msg.caption or "")
            )
        elif msg.document:
            await bot.send_document(
                GROUP_ID,
                document=msg.document.file_id,
                caption=prefix + (msg.caption or "")
            )
        elif msg.audio:
            await bot.send_audio(
                GROUP_ID,
                audio=msg.audio.file_id,
                caption=prefix + (msg.caption or "")
            )
        elif msg.voice:
            await bot.send_voice(
                GROUP_ID,
                voice=msg.voice.file_id,
                caption=prefix
            )
        elif msg.video_note:
            await bot.send_video_note(
                GROUP_ID,
                video_note=msg.video_note.file_id
            )
            if prefix:
                await bot.send_message(GROUP_ID, prefix)
        elif msg.sticker:
            await bot.send_sticker(GROUP_ID, sticker=msg.sticker.file_id)
            if prefix:
                await bot.send_message(GROUP_ID, prefix)
        else:
            await bot.copy_message(
                GROUP_ID,
                from_chat_id=msg.chat.id,
                message_id=msg.message_id,
                caption=prefix + (msg.caption or "") if msg.caption else prefix
            )

        await callback.message.edit_reply_markup(reply_markup=None)
        
        try:
            await bot.send_message(user_id, "✅ Ваш пост опубликован!")
        except:
            pass

        await callback.answer("✅ Опубликовано в группу")

    except Exception as e:
        logging.error(f"Ошибка публикации: {e}")
        await callback.answer("❌ Ошибка при публикации", show_alert=True)


@dp.callback_query(F.data.startswith("decline_"))
async def decline_handler(callback: CallbackQuery):
    if not await check_admin(callback):
        return

    user_id = int(callback.data.split("_")[1])
    
    await callback.message.delete()
    
    try:
        await bot.send_message(user_id, "❌ Ваш пост отклонён модератором")
    except:
        pass
    
    await callback.answer("❌ Пост отклонён")


@dp.callback_query(F.data.startswith("banselect_"))
async def ban_select_handler(callback: CallbackQuery):
    if not await check_admin(callback):
        return

    user_id = callback.data.split("_")[1]
    await callback.message.edit_reply_markup(
        reply_markup=get_ban_time_keyboard(user_id)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("banset_"))
async def ban_apply_handler(callback: CallbackQuery):
    if not await check_admin(callback):
        return

    _, uid, duration = callback.data.split("_")
    
    if duration == "forever":
        db.add_to_blacklist(uid)
        duration_text = "навсегда"
    else:
        days = int(duration)
        db.add_to_blacklist(uid, days)
        duration_text = f"{days} дн."

    await callback.message.edit_reply_markup(reply_markup=None)
    
    try:
        await bot.send_message(
            int(uid),
            f"🚫 Вы забанены модератором\nСрок: {duration_text}"
        )
    except:
        pass

    await callback.answer(f"🚫 Пользователь забанен на {duration_text}")


@dp.callback_query(F.data.startswith("cancelban_"))
async def cancel_ban_handler(callback: CallbackQuery):
    if not await check_admin(callback):
        return

    user_id = callback.data.split("_")[1]
    await callback.message.edit_reply_markup(
        reply_markup=get_moderation_keyboard(user_id)
    )
    await callback.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Бот запущен")
    print(f"👤 ADMIN ID: {ADMIN_ID}")
    print(f"👥 GROUP ID: {GROUP_ID}")
    print("-" * 30)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())