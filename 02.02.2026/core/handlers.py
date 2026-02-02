from aiogram import Router, types, Bot
from aiogram.filters import Command
from core.quiz import Quiz
from core.roulette import RussianRouletGame
import asyncio

class BotHandlers:
    def __init__(self, bot: Bot):
        self.router = Router()
        self.bot = bot

        self.quiz = Quiz()
        self.user_data = {}

        self.roulette_games = {}
        self.turn_tasks = {}

        self.register_handlers()

    def register_handlers(self):
        self.router.message.register(self.start_command, Command("start"))
        self.router.message.register(self.start_quiz, Command("quiz"))

        self.router.message.register(self.start_roulette, Command("roulette"))
        self.router.message.register(self.shoot_roulette, Command("shoot"))

    async def start_command(self, message: types.Message):
        await message.answer(
            "Привет 👋\n"
            "/quiz — викторина \n"
            "/roulette — русская рулетка "
        )

    async def start_quiz(self, message: types.Message):
        user_id = message.from_user.id
        self.user_data[user_id] = {"score": 0, "q_index": 0}
        await self.send_question(message.chat.id, user_id)

    async def send_question(self, chat_id, user_id):
        data = self.user_data.get(user_id)
        if not data:
            return
        question_data = self.quiz.get_question(data["q_index"])
        if not question_data:
            await self.finish_quiz(chat_id, user_id)
            return

        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text=opt, callback_data=f"quiz_{opt}")]
                for opt in question_data["options"]
            ]
        )

        await self.bot.send_message(chat_id, question_data["question"], reply_markup=keyboard)

    async def finish_quiz(self, chat_id, user_id):
        score = self.user_data[user_id]["score"]
        total = self.quiz.total_questions()
        await self.bot.send_message(chat_id, f"Викторина окончена!\nРезультат: {score} из {total}")
        del self.user_data[user_id]

    async def start_roulette(self, message: types.Message):
        user_id = message.from_user.id
        if user_id in self.roulette_games:
            await message.answer("Игра уже запущена!")
            return
        game = RussianRouletGame()
        self.roulette_games[user_id] = game
        await message.answer(
            f" Русская рулетка (2 игрока)\n"
            f"Игроки:\n1️ {game.players[0]}\n2️⃣ {game.players[1]}\n"
            f"Первый ход: {game.get_current_player()}\n 5 секунд на выстрел\n/shoot"
        )
        self.turn_tasks[user_id] = asyncio.create_task(self.turn_timer(message.chat.id, user_id))

    async def turn_timer(self, chat_id, user_id):
        await asyncio.sleep(5)
        game = self.roulette_games.get(user_id)
        if not game or not game.is_active:
            return
        loser = game.get_current_player()
        game.timeout()
        await self.bot.send_message(chat_id, f"Время вышло!\n {loser} проиграл!")
        self.cleanup_game(user_id)

    async def shoot_roulette(self, message: types.Message):
        user_id = message.from_user.id
        game = self.roulette_games.get(user_id)
        if not game:
            await message.answer("Сначала запусти игру через /roulette")
            return
        if not game.is_active:
            await message.answer("Игра уже завершена")
            return
        self.turn_tasks[user_id].cancel()
        current_player = game.get_current_player()
        result = game.shoot()
        if result == "boom":
            await message.answer(f"БАХ!\n {current_player} проиграл!")
            self.cleanup_game(user_id)
            return
        await message.answer(f" Пусто!\nСледующий ход: {game.get_current_player()}\n 5 секунд!")
        self.turn_tasks[user_id] = asyncio.create_task(self.turn_timer(message.chat.id, user_id))

    def cleanup_game(self, user_id):
        if user_id in self.turn_tasks:
            self.turn_tasks[user_id].cancel()
            del self.turn_tasks[user_id]
        if user_id in self.roulette_games:
            del self.roulette_games[user_id]