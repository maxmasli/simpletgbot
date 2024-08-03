from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.filters.command import Command
import random
import schedule

API_TOKEN = '7104745433:AAGaytVbeYBo55wBj1g6QdWIZ036zSMFluk'

isSwearsOn = True

swears = ["пидарас", "сука", "уебок", "хуепутало", "гандон", "чмо", "пидр", "гандапляс", "лох", "l", "лохозавр", "уебан", "саси", "дибил", "долбаеб", "даун", "нахуй"]
obr = ["бот", "ботяра", "ботик"]
swear_answers = ["пошел нахуй", "ты бля ахуел?", "ты чо сука", "иди ты нахуй пидр", "пиздец блять", "сука саси хуй", "лооох", "ты на кого батон крошиш", "ты ваще долбаеб?", "пиздец ты тупой"]
good_answer = ["Да, мой повелитель", "Да, отец"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Array to save chats IDs w/ the bot
ids = []

# Payment period info
firstDay = datetime.strptime('2024-07-30', '%Y-%m-%d')
payingPeriod = 31

# Command /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Здарова! Это бот крутой. Он стоит на сервере который ебать мы покупаем. Используй /help для получения списка команд.")
    ids.append(message.chat.id)
    logger.info(f"User {message.from_user.id} used /start")

# Command /help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    help_text = (
        "Список команд:\n"
        "/timer <минуты> <комментарий> - отправит комментарий через заданное количество минут.\n"
        "/nahui <имя> - отправляет сообщение 'Иди нахуй <имя>'.\n"
        "/help - показывает этот список команд.\n"
        "/swear - включает/выключает матерки.\n"
        "/paytime - отправляет количество дней до очередной оплаты сервера"
    )
    await message.reply(help_text)
    logger.info(f"User {message.from_user.id} used /help")

# Command /timer
@dp.message(Command("timer"))
async def set_timer(message: types.Message):
    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.reply("Использование: /timer <минуты> <комментарий>")
            return
        minutes = int(args[1])
        comment = args[2]
        await bot.send_message(message.chat.id, f"Таймер установлен на {minutes} минут. Я напомню: {comment}")
        logger.info(f"User {message.from_user.id} set a timer for {minutes} minutes with comment: {comment}")
        await asyncio.sleep(minutes * 60)
        await bot.send_message(message.chat.id, f"Таймер сработал! Напоминание: {comment}")
        logger.info(f"Timer finished for user {message.from_user.id} with comment: {comment}")
    except ValueError:
        await message.reply("Еблан, укажи корректное количество минут.")
        logger.warning(f"User {message.from_user.id} provided invalid minutes for /timer")

# Function to notify users about payment
async def rememberToPay():
    if (datetime.now() - firstDay).days % payingPeriod == 0:
        for id in ids: await bot.send_message(id, 'Сегодня вроде как нужно заплатить за сервак, расчехляйте свои кошельки и скидывайте бабос на карту Максу, заодно Михе Молодому Миксеру можете накинуть на карту за то, что он ночью нахуй бля сидел и переписывал таймер чтобы ахуенно было. Сколько кидать Михе и Максу, спросите у них сами, бот хз\n\n<i>Timer handler developed by</i> <b>$$$YungMixer$$$</b>', parse_mode="html")
    logger.info(f"Function rememberToPay() was executed")

# Command /paytime
@dp.message(Command("paytime"))
async def send_pay_time(message: types.Message):
    daysLeft = str(payingPeriod - (datetime.now() - firstDay).days)
    correctWords = " "
    if daysLeft in [i for i in range(2, 5)]: correctWords += "дня осталось"
    elif daysLeft == 1: correctWords += "день остался"
    else: correctWords += "дней осталось"
    await bot.send_message(message.chat.id, f"{daysLeft + correctWords} до очередной блядской оплаты сервака.\n\n<i>Это неточно, потому что эту хуйню Миша Молодой Миксер писал, он ваще хз когда там надо платить, но вроде мы с Максом все правильно посчитали.\n\nTimer handler developed by</i> <b>$$$YungMixer$$$</b>", parse_mode="html")
    logger.info(f"User {message.from_user.id} used /paytime")

# Command /nahui
@dp.message(Command("nahui"))
async def send_nahui(message: types.Message):
    try:
        name = message.text.split(maxsplit=1)[1]
        await bot.send_message(message.chat.id, f"Иди нахуй {name}")
        logger.info(f"User {message.from_user.id} sent 'Иди нахуй' to {name}")
    except IndexError:
        await message.reply("Использование: /nahui <имя>")
        logger.warning(f"User {message.from_user.id} used /nahui without providing a name")

# Command /swear
@dp.message(Command("swear"))
async def toggle_swear(message: types.Message):
    global isSwearsOn
    try:
        isSwearsOn = not isSwearsOn
        await bot.send_message(message.chat.id, "матерки: " + str(isSwearsOn))
        logger.info(f"User {message.from_user.id} turned swear words {'on' if isSwearsOn else 'off'}")
    except IndexError:
        await message.reply("Использование: /nahui <имя>")
        logger.warning(f"User {message.from_user.id} used /nahui without providing a name")



@dp.message(lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.id)
async def handle_reply_to_bot(message: types.Message):
    if (not isSwearsOn): return

    words = message.text.split(" ")
    hasSwear = False
    for w in words:
        hasSwear = hasSwear or w.lower() in swears

    if hasSwear:
        if message.from_user.id == 1161417419:
            await bot.send_message(message.chat.id, random.choice(good_answer))
            return

        answer = random.choice(swear_answers)
        await bot.send_message(message.chat.id, answer)
    logger.info(f"User {message.from_user.id} replied to bot's message with: {message.text}")


@dp.message()
async def handle_all_messages(message: types.Message):
    if (not isSwearsOn): return

    words = message.text.split(" ")
    hasObr = False
    hasSwear = False
    for w in words:
        hasObr = hasObr or w.lower() in obr
        hasSwear = hasSwear or w.lower() in swears

    if hasObr and hasSwear:
        if message.from_user.id == 1161417419:
            await bot.send_message(message.chat.id, random.choice(good_answer))
            return
        answer = random.choice(swear_answers)
        await bot.send_message(message.chat.id, answer)
    logger.info(f"User {message.from_user.id} wrote: {message.text}")

async def main():
    schedule.every().day.at("12:00").do(rememberToPay)
    await dp.start_polling(bot, skip_updates=True)

# Start polling
if __name__ == '__main__':
    asyncio.run(main())
