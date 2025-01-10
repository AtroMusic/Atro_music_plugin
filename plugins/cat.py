

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import time
from YukkiMusic import app

# ذخیره پیام‌ها و داده‌ها
hidden_messages = {}

@app.on_message(filters.command("نجوا") & filters.group)
async def handle_secret_message(bot: Client, message: Message):
    try:
        # تعیین کاربر هدف
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
        else:
            parts = message.text.split(" ", 1)
            if len(parts) < 2:
                return
            identifier = parts[1]
            target_user = await bot.get_users(identifier)

        target_user_id = target_user.id
        bot_username = (await bot.get_me()).username

        # ذخیره اطلاعات پیام
        hidden_messages[target_user_id] = {
            "group_id": message.chat.id,
            "group_title": message.chat.title,
            "sender_id": message.from_user.id,
            "sender_name": message.from_user.first_name,
            "timestamp": time.time()
        }

        # ارسال لینک به پیوی ربات
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📨 ارسال پیام", url=f"https://t.me/{bot_username}?start=send_{target_user_id}")]
        ])
        await message.reply_text(
            f"💌 برای ارسال پیام به {target_user.mention} لطفاً به پیوی من مراجعه کنید.",
            reply_markup=keyboard
        )
    except Exception as e:
        await message.reply_text(f"⚠️ خطا: {e}")

@app.on_message(filters.private & filters.command("start"))
async def start_private_message(bot: Client, message: Message):
    if message.text.startswith("/start send_"):
        target_user_id = int(message.text.split("_")[1])
        
        # بررسی وجود پیام ذخیره‌شده
        if target_user_id in hidden_messages:
            await message.reply_text(
                f"💬 لطفاً متن پیامی که می‌خواهید به {hidden_messages[target_user_id]['sender_name']} ارسال شود را بنویسید."
            )
            hidden_messages[target_user_id]["awaiting_message"] = True
