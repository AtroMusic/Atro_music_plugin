from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatAction
from TheApi import api
from YukkiMusic import app


@app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "Example:\n\n`/ai write simple website code using html css, js?`"
        )
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    results = api.chatgpt(user_input)
    await message.reply_text(results)


# __MODULE__ = "هوش مصنوعی"
__HELP__ = """
هوش مصنوعی

/advice - دریافت بیوگرافی
/ai  سؤال خود را با هوش مصنویی بپرسید
 
 سوال خود را با استفاده از گوگل بپرسید
  𝄞بارد 
/bard"""
