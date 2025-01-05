import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from pyrogram.errors import ChatAdminRequired

# تابع برای دریافت لینک گروه (خصوصی یا عمومی)
async def get_group_link(client: Client, chat_id: int):
    try:
        # بررسی اینکه آیا گروه عمومی است
        chat = await client.get_chat(chat_id)
        if chat.username:
            return f"https://t.me/{chat.username}"  # لینک عمومی گروه
        else:
            # تولید لینک دعوت برای گروه خصوصی
            return await client.export_chat_invite_link(chat_id)
    except ChatAdminRequired:
        print("ربات دسترسی ایجاد لینک را ندارد.")
        return None

# تابع ارسال پیام خروج کاربر
async def handle_user_left(client: Client, chat: ChatMemberUpdated):
    if chat.old_chat_member.status == "member" and chat.new_chat_member.status == "left":
        user = chat.old_chat_member.user
        chat_id = chat.chat.id
        chat_title = chat.chat.title

        # دریافت لینک گروه
        group_link = await get_group_link(client, chat_id)
        if not group_link:
            print("لینک گروه قابل بازیابی نیست.")
            return

        # ساخت متن پیام
        message_text = (
            f"سلام {user.first_name} عزیز!\n"
            f"متوجه شدیم که از گروه {chat_title} خارج شدی.\n"
            "از دستت ناراحتیم، ولی خوشحال می‌شیم برگردی! 🌟"
        )

        # دکمه شیشه‌ای با لینک گروه
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("برگشت به گروه", url=group_link)]
            ]
        )

        try:
            # ارسال پیام به پی‌وی کاربر
            await client.send_message(
                chat_id=user.id,
                text=message_text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"خطا در ارسال پیام به کاربر {user.id}: {e}")

# اتصال به event خروج کاربر از گروه
@app.on_chat_member_updated(filters.group)
async def track_user_left(client, chat_update: ChatMemberUpdated):
    await handle_user_left(client, chat_update)
