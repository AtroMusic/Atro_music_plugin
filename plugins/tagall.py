import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from YukkiMusic import app

SPAM_CHATS = []

# تابعی برای بررسی اینکه آیا کاربر فعال است
async def is_active_member(chat_id, user_id):
    # بررسی اینکه آیا کاربر پیام‌هایی اخیراً ارسال کرده است
    async for message in app.get_chat_history(chat_id, limit=5):  # چک کردن 5 پیام اخیر
        if message.from_user and message.from_user.id == user_id:
            return True
    return False

# تابع بررسی ادمین بودن
async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    return user_id in admin_ids

@app.on_message(
    filters.command(["تگ"], prefixes=["@", " "])  # بررسی دستور تگ
)
async def tag_active_users(_, message):
    # بررسی اینکه آیا کاربر ادمین است
    if not await is_admin(message.chat.id, message.from_user.id):
        return

    # بررسی اینکه دستور تگ به صورت ریپلای است یا خیر
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        return  # هیچ جوابی داده نمی‌شود در صورتی که پیام مستقیم نباشد

    # اگر دستور تگ به یک پیام ریپلای شده ارسال شده باشد
    if replied:
        usernum = 0
        usertxt = ""
        try:
            async for m in app.get_chat_members(message.chat.id):
                if m.user.is_deleted or m.user.is_bot:
                    continue

                # بررسی اینکه آیا کاربر فعال است
                if await is_active_member(message.chat.id, m.user.id):
                    usernum += 1
                    usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                    if usernum == 7:
                        await replied.reply_text(
                            usertxt, disable_web_page_preview=True
                        )
                        await asyncio.sleep(1)
                        usernum = 0
                        usertxt = ""
            if usernum != 0:
                await replied.reply_text(
                    usertxt, disable_web_page_preview=True
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
    else:
        # اگر دستور تگ به صورت مستقیم وارد شده باشد
        usernum = 0
        usertxt = ""
        text = message.text.split(None, 1)[1]
        try:
            async for m in app.get_chat_members(message.chat.id):
                if m.user.is_deleted or m.user.is_bot:
                    continue

                # بررسی اینکه آیا کاربر فعال است
                if await is_active_member(message.chat.id, m.user.id):
                    usernum += 1
                    usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                    if usernum == 7:
                        await app.send_message(
                            message.chat.id, f"{text}\n{usertxt}", disable_web_page_preview=True
                        )
                        await asyncio.sleep(2)
                        usernum = 0
                        usertxt = ""
            if usernum != 0:
                await app.send_message(
                    message.chat.id, f"{text}\n\n{usertxt}", disable_web_page_preview=True
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)

# __HELP__ = """
# **دستورات ربات تگ (فارسی)**

# - `تگ_همه_فعال` | `تگ_اعضای_فعال`: برای تگ کردن اعضای فعال گروه.

# **نکته:**
# - این دستور فقط افرادی را که اخیراً پیام ارسال کرده‌اند (فعال) تگ می‌کند.
# """
