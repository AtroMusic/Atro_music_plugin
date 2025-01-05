from pyrogram import filters
from pyrogram.enums import ChatAction

from YukkiMusic import app
from config import BANNED_USERS

import openai  # اضافه کردن کتابخانه OpenAI
openai.api_key = 'proj_IOtNiiYtjFJjurkhOpFmOJDQ'  # کلید API خود را اینجا قرار دهید

@app.on_message(filters.command(["chatgpt", "هوش مصنوعی", "سوال"], prefixes=['', '/']) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "❓ نمونه استفاده:\n\n`/chatgpt چگونه از حساب خود حفاظت کنیم؟`"
        )
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    try:
        # ایجاد پیام‌های گفتگو
        messages = [
            {"role": "system", "content": "You are an intelligent assistant."},
            {"role": "user", "content": user_input},
        ]
        # درخواست به OpenAI
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = chat.choices[0].message.content
        await message.reply_text(reply)
    except Exception as e:
        await message.reply_text(f"⚠️ خطا در پردازش درخواست: {e}")

# __MODULE__ = "چت جی‌پی‌تی 🤖"
# __HELP__ = """
# 📝 دستورات:
# /chatgpt [دستور] - سوال خود را از هوش مصنوعی بپرسید.
# /سوال [دستور] - سوال خود را بپرسید.
# """
