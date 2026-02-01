import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = '8520192253:AAH61nrR7xF9NnSur2uVO-8RgSmZjyXOlm8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

USER_STATUS = {} 
ALL_ORDERS = {}
TEMP_DATA = {} 


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Добавить заказ"))
    keyboard.add(types.KeyboardButton(text="Посмотреть заказы"))
    keyboard.add(types.KeyboardButton(text="Удаление"))
    
    await message.answer("Привет! Я бот для приема заказов.", reply_markup=keyboard)


@dp.message(lambda message: message.text == "Добавить заказ")
async def start_new_order(message: types.Message):
    user_id = message.from_user.id
    
    USER_STATUS[user_id] = 'awaiting_name' 
    
    await message.answer("Как тебя зовут?")


@dp.message(lambda message: USER_STATUS.get(message.from_user.id) == 'awaiting_name')
async def get_user_name(message: types.Message):
    user_id = message.from_user.id
    
    TEMP_DATA[user_id] = {'name': message.text}
    
    USER_STATUS[user_id] = 'awaiting_item'
    await message.answer("Что именно закажешь?")


@dp.message(lambda message: USER_STATUS.get(message.from_user.id) == 'awaiting_item')
async def get_order_item(message: types.Message):
    user_id = message.from_user.id
    
    TEMP_DATA[user_id]['item'] = message.text
    
    USER_STATUS[user_id] = 'awaiting_time'
    await message.answer("Напиши, к какому времени нужно приготовить?")


@dp.message(lambda message: USER_STATUS.get(message.from_user.id) == 'awaiting_time')
async def finalize_order(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in ALL_ORDERS:
        ALL_ORDERS[user_id] = []
        
    new_order = TEMP_DATA[user_id]
    new_order['time'] = message.text
    
    ALL_ORDERS[user_id].append(new_order)
    
    del USER_STATUS[user_id] 
    await message.answer("Ура! Заказ добавлен: " + new_order['item'] + " к " + new_order['time'])


@dp.message(lambda message: message.text == "Посмотреть заказы")
async def show_basket(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in ALL_ORDERS:
        await message.answer("У тебя еще нет заказов.")
        return
    
    if not ALL_ORDERS[user_id]:
        await message.answer("Заказов нет, корзина пустая!")
        return
    
    text = "Твои заказы:\n"
    for i, order in enumerate(ALL_ORDERS[user_id], 1):
        text += f"{i}. {order.get('item', '???')} (Имя: {order.get('name', 'N/A')}) на {order.get('time', 'Не указано')}\n"
    
    await message.answer(text)


@dp.message(lambda message: message.text == "Удаление")
async def delete_order_start(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in ALL_ORDERS or not ALL_ORDERS[user_id]:
        await message.answer("Нечего удалять, ты еще ничего не заказал!")
        return
    
    text = "Напиши номер заказа для удаления:\n"
    for i, order in enumerate(ALL_ORDERS[user_id], 1):
        text += f"{i}. {order['item']}\n"
    
    USER_STATUS[user_id] = 'awaiting_delete_num' 
    await message.answer(text)

async def main():
    print("Бот стартует...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())