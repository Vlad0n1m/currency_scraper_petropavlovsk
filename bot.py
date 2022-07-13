from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from scrapper import get_data

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start', 'help'])
async def process_start_command(message: types.Message):
    await message.reply("Чекер обменников в казахстане. Получить полный список обменников и курсов - /check")


@dp.message_handler(commands=['check'])
async def process_help_command(message: types.Message):
    exc_kb= ReplyKeyboardMarkup()
    global messages_dict
    messages_dict = get_data()
    for button in messages_dict:
        exc_kb.add(button)
    await message.reply("Обновленно! Выберите интересующий вас обменник из списка.", reply_markup=exc_kb)


@dp.message_handler()
async def echo_message(message: types.Message):
    try:
        await message.reply(messages_dict.get(message.text))
    except:
        await message.reply("/check")


    

if __name__ == '__main__':
    executor.start_polling(dp)