from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

TOKEN = "8765311580:AAG2AAcGqfGdh2om0gCC4LysryRVFA7gLSg"
ARCHIVE_CHAT_ID = -1003914108879

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ARCHIVE", callback_data="archive")]
    ])

@dp.message()
async def send_task(message: types.Message):
    await message.reply(
        "Task\nStatus: NEW",
        reply_markup=get_keyboard()
    )

@dp.callback_query(lambda c: c.data == "archive")
async def archive_task(callback: types.CallbackQuery):

    # беремо повідомлення користувача
    user_msg = callback.message.reply_to_message

    # пересилаємо в архів
    await bot.forward_message(
        ARCHIVE_CHAT_ID,
        callback.message.chat.id,
        user_msg.message_id
    )

    # видаляємо повідомлення бота
    await callback.message.delete()

    # видаляємо повідомлення користувача
    try:
        await bot.delete_message(
            callback.message.chat.id,
            user_msg.message_id
        )
    except:
        pass

    await callback.answer("Moved to archive")
async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())