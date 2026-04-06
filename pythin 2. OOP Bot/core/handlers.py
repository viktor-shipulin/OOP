from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from core.quiz import Quiz


class BotHandlers:
    def __init__(self, bot: Bot):
        self.router = Router()
        self.quiz = Quiz()
        self.user_data = {}
        self.bot = bot
        self.register_handlers()

    def register_handlers(self):
        self.router.message.register(self.start_command, Command("start"))
        self.router.message.register(self.quiz_start, Command("quiz"))
        self.router.callback_query.register(self.handle_answer)

    async def start_command(self, message: types.Message):
        await message.answer("Привет!\nНапиши /quiz чтобы начать игру")

    async def quiz_start(self, message: types.Message):
        user_id = message.from_user.id
        self.user_data[user_id] = {"score": 0, "q_index": 0}
        await self.send_question(message.chat.id, user_id)

    async def send_question(self, chat_id, user_id):
        data = self.user_data.get(user_id)
        question_data = self.quiz.get_question(data["q_index"])

        if not question_data:
            await self.end_quiz(chat_id, user_id)
            return

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=opt, callback_data=opt)]
                for opt in question_data["option"]
            ]
        )

        await self.bot.send_message(chat_id, question_data["question"], reply_markup=keyboard)

    async def handle_answer(self, callback: CallbackQuery):
        user_id = callback.from_user.id
        selected_answer = callback.data
        data = self.user_data.get(user_id)

        if not data:
            await callback.answer("Сначала начни игру через /quiz")
            return

        question_data = self.quiz.get_question(data["q_index"])

        if selected_answer == question_data["correct"]:
            data["score"] += 1

        data["q_index"] += 1

        await callback.answer("Ответ принят")
        await self.send_question(callback.message.chat.id, user_id)

    async def end_quiz(self, chat_id, user_id):
        score = self.user_data[user_id]["score"]
        await self.bot.send_message(chat_id, f"Игра окончена! Твой результат: {score}")
        del self.user_data[user_id]