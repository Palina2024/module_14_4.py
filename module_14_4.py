from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import initiate_db, get_all_products



api = '7617377965:AAGutcKCqCcKpJnC-vS2PtQD9VjMYuF4rPM'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

initiate_db()
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text='Информация'),
        KeyboardButton(text='Рассчитать'),
        KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True
)

calc_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')],
    ], resize_keyboard=True
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')],
    ], resize_keyboard=True
)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        id, title, description, price = product
        with open(f'files/{id}.png', "rb") as img:
            await message.answer_photo(img, f'Название: {title}\nОписание: {description}\nЦена: {price}')
    await message.answer('Выберите продукт для покупки:', reply_markup=buy_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')



@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=calc_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора для рассчета нормы калорий для женщин: '
                              '10 x вес(кг) + 6,25 x рост(см) – 5 x возраст(г) – 161.')



@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await message.answer('Введите свой рост:')
        await UserState.growth.set()
    else:
        await message.answer('Пожалуйста, введите корректное числовое значение возраста.')

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес:')
        await UserState.weight.set()
    else:
        await message.answer('Пожалуйста, введите корректное числовое значение для роста.')

@dp.message_handler(state=UserState.weight)
async def set_calories(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(weight=message.text)
        data = await state.get_data()
        age = int(data['age'])  # возраст
        growth = int(data['growth']) # рост
        weight = int(data['weight']) # вес
        # Пример формулы для женщин
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

        await message.answer(f'Ваша норма калорий: {calories} ккал.')
        await state.finish()
    else:
        await message.answer('Пожалуйста, введите корректное числовое значение для веса.')

@dp.message_handler(commands=['start'])
async def start_messages(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=start_kb)

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)