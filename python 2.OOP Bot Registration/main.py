from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

from core.bot import TelegramBot
from core.database import UniversityDB 


db = UniversityDB()

class Form(StatesGroup):
    full_name = State()
    age = State()
    group_name = State()
    phone = State()
    email = State()
    github_link = State()
    programming_lang = State()
    experience = State()
    hobby = State()

router = Router()
@router.message(Command("register"))
async def start_reg(message: types.Message, state: FSMContext):
    await message.answer("Начинаем регистрацию! 📝\nВведите ваше ФИО:")
    await state.set_state(Form.full_name)

@router.message(Form.full_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Пожалуйста, введите возраст цифрами:")
    await state.update_data(age=int(message.text))
    await message.answer("Назовите вашу группу:")
    await state.set_state(Form.group_name)

@router.message(Form.group_name)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group_name=message.text)
    await message.answer("Ваш номер телефона:")
    await state.set_state(Form.phone)

@router.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Ваш email:")
    await state.set_state(Form.email)

@router.message(Form.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Пришлите ссылку на ваш GitHub:")
    await state.set_state(Form.github_link)

@router.message(Form.github_link)
async def process_github(message: types.Message, state: FSMContext):
    await state.update_data(github_link=message.text)
    await message.answer("Ваш основной язык программирования?")
    await state.set_state(Form.programming_lang)

@router.message(Form.programming_lang)
async def process_lang(message: types.Message, state: FSMContext):
    await state.update_data(programming_lang=message.text)
    await message.answer("Ваш опыт в разработке (например: новичок или 2 года):")
    await state.set_state(Form.experience)

@router.message(Form.experience)
async def process_exp(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Какое у вас хобби?")
    await state.set_state(Form.hobby)

@router.message(Form.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    
    data = await state.get_data()
    data['user_id'] = message.from_user.id 
    
    db.add_student(data) 
    
    await message.answer(f"Поздравляю, {data['full_name']}! 🎉\nРегистрация завершена")
    await state.clear()


async def main():
    bot = TelegramBot()
    bot.dp.include_router(router) 
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")