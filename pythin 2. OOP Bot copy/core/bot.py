from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from сonfigure import BOT_Token
from core.handlers import BotHandlers
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=BOT_Token)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.handlers = BotHandlers(self.bot)
        self.dp.include_router(self.handlers.router)

    async def start(self):
        await self.dp.start_polling(self.bot) 