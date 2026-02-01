from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
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
        await message.answer("Привет! Викторина из 15 вопросов готова.\nНапиши /quiz для начала!")

    async def quiz_start(self, message: types.Message):
        user_id = message.from_user.id
        self.user_data[user_id] = {"score": 0, "wrong": 0, "q_index": 0}
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

        caption_text = f"Вопрос {data['q_index'] + 1}/15: {question_data['question']}"
        photo = FSInputFile(question_data["image"])

        await self.bot.send_photo(
            chat_id, 
            photo=photo, 
            caption=caption_text, 
            reply_markup=keyboard
        )

    async def handle_answer(self, callback: CallbackQuery):
        user_id = callback.from_user.id
        selected_answer = callback.data
        data = self.user_data.get(user_id)

        if not data:
            return

        question_data = self.quiz.get_question(data["q_index"])

        if selected_answer == question_data["correct"]:
            data["score"] += 1
        else:
            data["wrong"] += 1

        data["q_index"] += 1
        
        await callback.message.delete()
        await self.send_question(callback.message.chat.id, user_id)

    async def end_quiz(self, chat_id, user_id):
        res = self.user_data[user_id]
        await self.bot.send_message(
            chat_id, 
            f"Ура! Тест пройден.\n Правильно: {res['score']}\n Ошибок: {res['wrong']}"
        )
        del self.user_data[user_id]