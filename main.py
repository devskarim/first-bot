import asyncio
import wikipedia
import html
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.enums import ChatAction
from deep_translator import GoogleTranslator
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

wikipedia.set_lang("uz")
translator = GoogleTranslator(source="auto", target="uz")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Assalomu alaykum {message.from_user.first_name}!\n"
        "Xush kelibsiz.\nKo'proq ma'lumot olish uchun /help buyrug'ini bosing."
    )


@dp.message(Command("help"))
async def command(message: Message):
    await message.reply(
        "Bu bot 3 xil vazifa uchun mo'jalangan:"
        "\nWikipediya qidirish: /wiki <so'z>"
        "\nTarjima: /dic <so'z>"
        "\nEcho: /echo <matn>"
    )


@dp.message(Command("wiki"))
async def wiki(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Iltimos, qidiriladigan so'zni yozing. Masalan: /wiki python")
        return

    query = parts[1]
	
	
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)


    try:
        result = await asyncio.to_thread(wikipedia.summary, query, sentences=3)

        safe_query = html.escape(query)
        safe_result = html.escape(result)

        await message.reply(f"<b>{safe_query}</b>\n\n{safe_result}", parse_mode="HTML")

    except wikipedia.exceptions.DisambiguationError as e:
        await message.reply("Bu mavzu aniq emas. Ba'zi variantlar:\n" + "\n".join(e.options[:5]))
    except wikipedia.exceptions.PageError:
        await message.answer("Bu mavzu bo'yicha ma'lumot topilmadi.")


@dp.message(Command("dic"))
async def translate_handler(message: Message):
    args = message.text.split(" ", 2)  
    
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    
    if len(args) == 1:
        await message.reply("Foydalanish: /dic <til> <matn>\n\nMisol: `/dic ru Hello world!`")
        return

   
    if len(args) == 2:
        lang = "en"
        text = args[1]
    else:
        lang = args[1]   
        text = args[2]  

    try:
        translated = GoogleTranslator(source="auto", target=lang).translate(text)
        await message.reply(f"Tarjima:\n{translated}")
    except Exception as e:
        await message.reply(f"Xatolik: {e}")




@dp.message(Command('echo'))

async def echo_word(message: Message): 
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Iltimos, echo so'zni yozing. Masalan: /echo (so'z)")
        return

    query = parts[1]
    
    await message.reply(f"Siz yozdingiz {query}")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
