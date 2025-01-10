
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import time
from YukkiMusic import app

# ذخیره اطلاعات پیام‌ها
hidden_messages = {}

@app.on_message(filters.command("نجوا") & filters.group)
async def handle_secret_message(bot: Client, message: Message):
    try:
        # بررسی شرایط صحیح ارسال دستور
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
        else:
            parts = message.text.split(" ", 1)
            if len(parts) < 2:
                return
            identifier = parts[1]
            target_user = await bot.get_users(identifier)

        target_user_id = target_user.id
        target_username = target_user.mention

        # ذخیره اطلاعات پیام برای ارسال به پیوی
        hidden_messages[target_user_id] = {
            "group_id": message.chat.id,
            "group_title": message.chat.title,
            "sender_id": message.from_user.id,
            "sender_name": message.from_user.first_name,
            "target_username": target_username,
            "timestamp": time.time()
        }

        # ایجاد لینک مستقیم به پیوی ربات
        bot_username = (await bot.get_me()).username
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📨 ارسال پیام", url=f"https://t.me/{bot_username}?start=send_{target_user_id}")]
        ])

        await message.reply_text(
            f"💌 برای ارسال پیام به {target_username} لطفاً به پیوی من مراجعه کنید و متن خود را ارسال کنید.",
            reply_markup=keyboard
        )

    except Exception as e:
        await message.reply_text(f"⚠️ خطا: {e}")


@app.on_message(filters.private & filters.command("start"))
async def start_private_message(bot: Client, message: Message):
    command_data = message.text.split("_")

    if len(command_data) == 2 and command_data[1].isdigit():
        target_user_id = int(command_data[1])
        
        # بررسی وجود اطلاعات پیام
        if target_user_id in hidden_messages:
            await message.reply_text(
                f"💬 لطفاً متن پیامی که می‌خواهید به {hidden_messages[target_user_id]['target_username']} ارسال شود را وارد کنید."
            )
            hidden_messages[target_user_id]["awaiting_message"] = True


@app.on_message(filters.private & filters.text)
async def receive_private_message(bot: Client, message: Message):
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
    target_username = data["target_username"]

    # ارسال پیام به گروه و تگ کاربر هدف
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👀 خواندن پیام", callback_data=f"read_{user_id}"),
         InlineKeyboardButton("🗑️ حذف پیام", callback_data=f"delete_{user_id}")]
    ])

    await bot.send_message(
        group_id,
        f"📨 پیام جدید برای {target_username}:\n\n"
        f"💬 {message.text}",
        reply_markup=keyboard
    )

    await message.reply_text("✅ پیام شما به گروه ارسال شد.")

    # بروزرسانی اطلاعات پیام
    hidden_messages[user_id]["awaiting_message"] = False


@app.on_callback_query(filters.regex(r"read_"))
async def handle_read_message(bot: Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    data = hidden_messages.get(user_id)

    if not data:
        return await query.answer("⛔ پیام یافت نشد.", show_alert=True)

    if query.from_user.id != user_id:
        return await query.answer("🤭 این پیام برای شما نیست!", show_alert=True)

    await query.answer("✅ پیام مشاهده شد.")
    await query.message.edit_text(f"👀 پیام توسط {data['target_username']} مشاهده شد.")
    # اطلاع به ارسال‌کننده
    sender_id = data["sender_id"]
    await bot.send_message(sender_id, "📩 پیام شما مشاهده شد.")


@app.on_callback_query(filters.regex(r"delete_"))
async def handle_delete_message(bot: Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    data = hidden_messages.get(user_id)

    if not data:
        return await query.answer("⛔ پیام یافت نشد.", show_alert=True)

    if query.from_user.id != user_id:
        return await query.answer("🤭 این پیام برای شما نیست!", show_alert=True)

    await query.message.delete()
    await query.answer("🗑️ پیام حذف شد.")
