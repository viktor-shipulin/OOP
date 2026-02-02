import asyncio
from aiogram import Bot, Dispatcher
from core.bot import BotHandlers
from configure import BOT_TOKEN

async def main():
    bot = Bot(token=BOT_TOKEN)
    handlers = BotHandlers(bot)

    dp = Dispatcher()
    dp.include_router(handlers.router)

    print("запущен...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())