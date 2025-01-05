from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from pyrogram.errors import ChatAdminRequired, PeerIdInvalid
from YukkiMusic import app  # مطمئن شوید app وارد شده است.

# تابع دریافت لینک گروه
async def get_group_link(client, chat_id):
    try:
        chat = await client.get_chat(chat_id)
        if chat.username:
            return f"https://t.me/{chat.username}"
        else:
            return await client.export_chat_invite_link(chat_id)
    except ChatAdminRequired:
        print("ربات دسترسی لازم برای ایجاد لینک دعوت ندارد.")
        return None
    except Exception as e:
        print(f"خطا در دریافت لینک گروه: {e}")
        return None

# تابع ارسال پیام به کاربر
async def send_left_message(client, user, chat_title, group_link):
    try:
        message_text = (
            f"سلام {user.first_name} عزیز!\n"
            f"دیدیم که از گروه {chat_title} خارج شدی.\n"
            "اگر پشیمون شدی، می‌تونی برگردی پیش ما! 🌟"
        )
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("بازگشت به گروه", url=group_link)]]
        )
        await client.send_message(
            chat_id=user.id,
            text=message_text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
        print(f"پیام خروج به {user.id} ارسال شد.")
    except PeerIdInvalid:
        print(f"کاربر {user.id} ربات را استارت نکرده است.")
    except Exception as e:
        print(f"خطا در ارسال پیام خروج به {user.id}: {e}")

# رویداد برای ترک کاربر
@app.on_chat_member_updated(filters.group)
async def track_user_left(client, chat_update: ChatMemberUpdated):
    try:
        if chat_update.old_chat_member and chat_update.new_chat_member:
            if (
                chat_update.old_chat_member.status == "member"
                and chat_update.new_chat_member.status == "left"
            ):
                user = chat_update.old_chat_member.user
                chat = chat_update.chat
                group_link = await get_group_link(client, chat.id)
                if not group_link:
                    print("لینک گروه در دسترس نیست.")
                    return

                await send_left_message(client, user, chat.title, group_link)
    except Exception as e:
        print(f"خطا در رویداد ترک کاربر: {e}")
