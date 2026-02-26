import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import os

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@aiwork_ru"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def check_sub(user_id):
    member = await bot.get_chat_member(CHANNEL, user_id)
    return member.status in ["member", "creator", "administrator"]

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if await check_sub(message.from_user.id):
        await show_menu(message)
    else:
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Подписаться", url="https://t.me/aiwork_ru"))
        kb.add(InlineKeyboardButton("Проверить подписку", callback_data="check_sub"))
        await message.answer("Чтобы получить доступ к AI-меню, подпишитесь на канал.", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def process_check(callback_query: types.CallbackQuery):
    if await check_sub(callback_query.from_user.id):
        await show_menu(callback_query.message)
    else:
        await callback_query.answer("Вы не подписаны!", show_alert=True)

async def show_menu(message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎨 Kandinsky", url="https://t.me/kandinsky21_bot"))
    kb.add(InlineKeyboardButton("🧠 GigaChat", url="https://t.me/gigachat_bot"))
    kb.add(InlineKeyboardButton("🤖 BotHub", url="https://t.me/bothub_chat"))
    await message.answer("Выберите AI инструмент:", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
