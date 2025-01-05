from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from pyrogram.errors import ChatAdminRequired
from YukkiMusic import app  # شیء app را وارد کنید.

# تابع برای دریافت لینک گروه
async def get_group_link(client, chat_id):
    try:
        chat = await client.get_chat(chat_id)
        if chat.username:
            return f"https://t.me/{chat.username}"
        else:
            return await client.export_chat_invite_link(chat_id)
    except ChatAdminRequired:
        print("ربات دسترسی لازم برای ایجاد لینک را ندارد.")
        return None

# تابع ارسال پیام خروج کاربر
async def handle_user_left(client, chat):
    # بررسی اینکه old_chat_member و new_chat_member موجود هستند یا خیر
    if chat.old_chat_member and chat.new_chat_member:
        if chat.old_chat_member.status == "member" and chat.new_chat_member.status == "left":
            user = chat.old_chat_member.user
            chat_id = chat.chat.id
            chat_title = chat.chat.title

            group_link = await get_group_link(client, chat_id)
            if not group_link:
                print("لینک گروه در دسترس نیست.")
                return

            message_text = (
                f"سلام {user.first_name} عزیز!\n"
                f"دیدیم که از گروه {chat_title} خارج شدی.\n"
                "اگر پشیمون شدی، برگرد پیش ما! 🌟"
            )
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("بازگشت به گروه", url=group_link)]]
            )
            try:
                await client.send_message(
                    chat_id=user.id,
                    text=message_text,
                    reply_markup=keyboard,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"خطا در ارسال پیام به {user.id}: {e}")

# اتصال به event خروج کاربر
@app.on_chat_member_updated(filters.group)
async def track_user_left(client, chat_update: ChatMemberUpdated):
    # اطمینان از اینکه old_chat_member و new_chat_member موجود هستند
    if chat_update.old_chat_member and chat_update.new_chat_member:
        await handle_user_left(client, chat_update)
