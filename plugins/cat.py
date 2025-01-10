
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import time
from YukkiMusic import app

# ذخیره پیام‌ها و گزارش فعالیت‌ها
hidden_messages = {}
activity_logs = []

@app.on_message(filters.command("نجوا") & filters.group)
async def send_secret_message(bot, message: Message):
    try:
        # بررسی صحت شرایط ارسال پیام
        if not message.reply_to_message and len(message.command) == 1:
            return  # بدون پاسخ به کاربر

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.mention  # دریافت نام کاربر برای تگ کردن
        else:
            parts = message.text.split(" ", 1)
            if len(parts) < 2:
                return  # بدون پاسخ به کاربر
            user_identifier = parts[1]
            if user_identifier.isdigit():
                user_id = int(user_identifier)
                user = await bot.get_users(user_id)
                username = user.mention
            else:
                user = await bot.get_users(user_identifier)
                user_id = user.id
                username = user.mention

        if user_id == message.from_user.id:
            return  # بدون پاسخ به کاربر

        # ذخیره اطلاعات پیام
        hidden_messages[user_id] = {
            "sender_id": message.from_user.id,
            "sender_name": message.from_user.first_name,
            "group_id": message.chat.id,
            "group_title": message.chat.title,
            "username": username,
            "timestamp": time.time()
        }

        # ایجاد لینک مستقیم به پیوی ربات
        bot_username = (await bot.get_me()).username
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📨 ارسال پیام", url=f"https://t.me/{bot_username}?start=send_{user_id}")]
        ])
        await message.reply_text(
            f"💌 برای ارسال پیام به {username} لطفاً روی دکمه زیر کلیک کرده و متن پیام را در پیوی ارسال کنید.",
            reply_markup=keyboard
        )
        activity_logs.append(f"📌 {message.from_user.first_name} در گروه {message.chat.title} یک پیام نجوا ارسال کرد.")

    except Exception as e:
        await message.reply_text(f"⚠️ خطایی رخ داد: {str(e)}")


@app.on_message(filters.private & filters.command("start"))
async def start_private_message(bot, message: Message):
    command_data = message.text.split("_")

    if len(command_data) == 2 and command_data[1].isdigit():
        user_id = int(command_data[1])
        await message.reply_text(
            f"💬 لطفاً متن پیامی که می‌خواهید به {hidden_messages[user_id]['username']} ارسال شود را وارد کنید."
        )
        hidden_messages[user_id]["awaiting_message"] = True


@app.on_message(filters.private & filters.text)
async def receive_private_message(bot, message: Message):
    sender_id = message.from_user.id
    target_data = None

    # بررسی پیام مرتبط
    for user_id, data in hidden_messages.items():
        if data.get("awaiting_message") and data["sender_id"] == sender_id:
            target_data = (user_id, data)
            break

    if not target_data:
        return await message.reply_text("⛔ پیامی مرتبط با این کاربر یافت نشد.")

    user_id, data = target_data
    group_id = data["group_id"]
    group_title = data["group_title"]
    username = data["username"]

    # ارسال پیام به گروه و تگ کاربر
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👀 خواندن پیام", callback_data=f"read_{user_id}"),
         InlineKeyboardButton("🗑️ حذف پیام", callback_data=f"delete_{user_id}")]
    ])
    sent_message = await bot.send_message(
        group_id,
        f"📨 پیام جدید برای {username} در گروه {group_title}:\n\n"
        f"💬 {message.text}",
        reply_markup=keyboard
    )

    # ذخیره اطلاعات پیام
    hidden_messages[user_id]["message_id"] = sent_message.message_id
    hidden_messages[user_id]["message_text"] = message.text
    hidden_messages[user_id]["awaiting_message"] = False
    activity_logs.append(f"📌 پیام مخفی از {message.from_user.first_name} به {user_id} ارسال شد.")
