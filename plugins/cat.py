
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import time
from YukkiMusic import app


# ذخیره پیام‌ها
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
        
        if target_user_id in hidden_messages:
            await message.reply_text(
                f"💬 لطفاً متن پیامی که می‌خواهید به {hidden_messages[target_user_id]['sender_name']} ارسال شود را بنویسید."
            )
            hidden_messages[target_user_id]["awaiting_message"] = True
        else:
            await message.reply_text("⛔ پیامی مرتبط با این کاربر یافت نشد.")

@app.on_message(filters.private & filters.text)
async def receive_private_message(bot: Client, message: Message):
    for target_user_id, data in hidden_messages.items():
        if "awaiting_message" in data and data["awaiting_message"]:
            group_id = data["group_id"]
            group_title = data["group_title"]
            sender_name = data["sender_name"]

            # ارسال پیام به گروه و تگ کاربر هدف
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("👀 خواندن پیام", callback_data=f"read_{target_user_id}"),
                 InlineKeyboardButton("🗑 حذف پیام", callback_data=f"delete_{target_user_id}")]
            ])
            
            await bot.send_message(
                group_id,
                f"📢 پیام جدید از {sender_name} برای {await bot.get_users(target_user_id).mention}:\n\n{message.text}",
                reply_markup=keyboard
            )
            
            # ارسال تایید به فرستنده
            await message.reply_text("✅ پیام شما ارسال شد.")
            
            # به‌روزرسانی داده‌ها
            hidden_messages[target_user_id].update({
                "message_text": message.text,
                "awaiting_message": False
            })
            break

@app.on_callback_query(filters.regex(r"read_"))
async def handle_read_message(bot: Client, query: CallbackQuery):
    target_user_id = int(query.data.split("_")[1])

    if query.from_user.id == target_user_id:
        await query.message.edit_text("📖 پیام مشاهده شد.")
        sender_id = hidden_messages[target_user_id]["sender_id"]
        
        # اطلاع‌رسانی به فرستنده
        await bot.send_message(sender_id, f"👁 پیام شما توسط {query.from_user.first_name} مشاهده شد.")
    else:
        await query.answer("😅 این پیام برای شما نیست!", show_alert=True)

@app.on_callback_query(filters.regex(r"delete_"))
async def handle_delete_message(bot: Client, query: CallbackQuery):
    target_user_id = int(query.data.split("_")[1])

    if query.from_user.id == target_user_id:
        await query.message.delete()
        await query.answer("🗑 پیام حذف شد.")
    else:
        await query.answer("😂 شما اجازه حذف این پیام را ندارید!", show_alert=True)

app.run()
