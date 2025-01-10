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
        # بررسی شرایط درست بودن پیام
        if not message.reply_to_message and len(message.command) == 1:
            return  # بدون پاسخ به کاربر

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            parts = message.text.split(" ", 1)
            if len(parts) < 2:
                return  # بدون پاسخ به کاربر
            user_identifier = parts[1]
            if user_identifier.isdigit():
                user_id = int(user_identifier)
            else:
                user = await bot.get_users(user_identifier)
                user_id = user.id

        if user_id == message.from_user.id:
            return  # بدون پاسخ به کاربر

        # ذخیره اطلاعات پیام
        hidden_messages[user_id] = {
            "sender_id": message.from_user.id,
            "sender_name": message.from_user.first_name,
            "group_id": message.chat.id,
            "group_title": message.chat.title,
            "timestamp": time.time()
        }

        # ارسال پیام به ارسال‌کننده
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📨 ارسال پیام", url=f"tg://user?id={bot.me.id}")]
        ])
        await message.reply_text(
            f"💌 پیامی که می‌خواهید به کاربر ارسال کنید را در پیوی من ارسال کنید.\n\n"
            f"📍 گیرنده: {user_id}",
            reply_markup=keyboard
        )
        activity_logs.append(f"📌 {message.from_user.first_name} در گروه {message.chat.title} یک پیام نجوا ارسال کرد.")

    except Exception as e:
        await message.reply_text(f"⚠️ خطایی رخ داد: {str(e)}")


@app.on_message(filters.private & filters.text)
async def receive_private_message(bot, message: Message):
    sender_id = message.from_user.id

    # بررسی پیام
    target_data = None
    for user_id, data in hidden_messages.items():
        if data["sender_id"] == sender_id:
            target_data = (user_id, data)
            break

    if not target_data:
        return await message.reply_text("⛔ پیامی مرتبط با این کاربر یافت نشد.")

    user_id, data = target_data
    group_id = data["group_id"]
    group_title = data["group_title"]

    # ارسال پیام به گروه
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👀 خواندن پیام", callback_data=f"read_{user_id}"),
         InlineKeyboardButton("🗑️ حذف پیام", callback_data=f"delete_{user_id}")]
    ])
    sent_message = await bot.send_message(
        group_id,
        f"📨 پیام جدید برای {message.from_user.mention} در گروه {group_title}:\n\n"
        f"💬 {message.text}",
        reply_markup=keyboard
    )

    # ذخیره اطلاعات پیام
    hidden_messages[user_id]["message_id"] = sent_message.message_id
    hidden_messages[user_id]["message_text"] = message.text

    activity_logs.append(f"📌 پیام مخفی از {message.from_user.first_name} به {user_id} ارسال شد.")


@app.on_callback_query(filters.regex(r"read_"))
async def read_message(bot, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    sender_id = hidden_messages.get(user_id, {}).get("sender_id")

    if query.from_user.id != user_id:
        return await query.answer("❌ شما اجازه مشاهده این پیام را ندارید.", show_alert=True)

    await query.message.edit_text("✅ پیام شما خوانده شد.")
    await bot.send_message(sender_id, f"📥 پیام شما توسط {query.from_user.first_name} خوانده شد.")
    activity_logs.append(f"👀 پیام از {sender_id} توسط {query.from_user.first_name} مشاهده شد.")


@app.on_callback_query(filters.regex(r"delete_"))
async def delete_message(bot, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])

    if query.from_user.id != user_id:
        return await query.answer("❌ شما اجازه حذف این پیام را ندارید.", show_alert=True)
        await query.message.delete()
        del hidden_messages[user_id]
        await query.answer("🗑️ پیام با موفقیت حذف شد.")
        activity_logs.append(f"🗑️ پیام برای {user_id} حذف شد.")


@app.on_callback_query(filters.regex(r"logs"))
async def view_logs(bot, query: CallbackQuery):
    if query.from_user.id not in [admin.id for admin in await bot.get_chat_administrators(query.message.chat.id)]:
        return await query.answer("❌ فقط مدیران می‌توانند گزارش‌ها را مشاهده کنند.", show_alert=True)

    if not activity_logs:
        return await query.answer("📄 هنوز هیچ فعالیتی ثبت نشده است.", show_alert=True)

    log_text = "\n".join(activity_logs[-10:])  # نمایش آخرین ۱۰ فعالیت
    await query.message.reply_text(f"📊 گزارش فعالیت‌ها:\n\n{log_text}")


@app.on_message(filters.command("گزارش‌ها") & filters.group)
async def show_logs_command(bot, message: Message):
    if message.from_user.id not in [admin.id for admin in await bot.get_chat_administrators(message.chat.id)]:
        return await message.reply_text("❌ فقط مدیران می‌توانند این دستور را اجرا کنند.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 مشاهده گزارش‌ها", callback_data="logs")]
    ])
    await message.reply_text("📄 برای مشاهده گزارش‌ها روی دکمه زیر کلیک کنید.", reply_markup=keyboard)
