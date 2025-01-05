'''import datetime
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app
from YukkiMusic.utils.database import get_welcome, set_welcome, del_welcome
from YukkiMusic.utils.permissions import adminsOnly

# مدیریت خوش‌آمدگویی
async def send_welcome_message(chat, user_id):
    welcome, raw_text, file_id = await get_welcome(chat.id)
    if not raw_text:
        return

    user = await app.get_users(user_id)
    text = raw_text.replace("{GROUPNAME}", chat.title).replace("{NAME}", user.mention)
    text = text.replace("{DATE}", datetime.datetime.now().strftime("%Y-%m-%d"))

    await app.send_message(chat.id, text)

# مدیریت لفت‌بک (خروج از گروه)
@app.on_chat_member_updated(filters.group, group=6)
async def handle_user_events(_, update: ChatMemberUpdated):
    chat = update.chat
    old_status = update.old_chat_member.status
    new_status = update.new_chat_member.status

    # ارسال پیام خوش‌آمدگویی
    if old_status in [CMS.LEFT, CMS.RESTRICTED] and new_status == CMS.MEMBER:
        await send_welcome_message(chat, update.new_chat_member.user.id)

    # مدیریت خروج کاربران
    if old_status == CMS.MEMBER and new_status == CMS.LEFT:
        member = update.old_chat_member.user
        try:
            # ساخت لینک دعوت به گروه
            group_link = await app.create_chat_invite_link(chat.id)
            # ارسال پیام در پی‌وی کاربر
            await app.send_message(
                member.id,
                f"سلام {member.first_name}!\n"
                f"شما از گروه {chat.title} خارج شده‌اید.\n"
                "برای بازگشت به گروه روی دکمه زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("بازگشت به گروه", url=group_link.invite_link)]]
                ),
            )
        except Exception as e:
            print(f"Error sending private message: {e}")

# دستور تنظیم پیام خوش‌آمد (فقط در گروه)
@app.on_message(filters.command("تنظیم_خوشامد") & filters.group)
@adminsOnly("can_change_info")
async def set_welcome_func(_, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply_text("لطفاً به یک پیام (متن، عکس یا GIF) پاسخ دهید.")

    welcome_type = None
    file_id = None
    text = None

    if replied.animation:
        welcome_type = "Animation"
        file_id = replied.animation.file_id
        text = replied.caption
    elif replied.photo:
        welcome_type = "Photo"
        file_id = replied.photo.file_id
        text = replied.caption
    elif replied.text:
        welcome_type = "Text"
        text = replied.text

    if not text:
        return await message.reply_text("لطفاً یک پیام با متن مشخص ارسال کنید.")

    await set_welcome(message.chat.id, welcome_type, text, file_id)
    await message.reply_text("پیام خوش‌آمدگویی با موفقیت تنظیم شد.")

# دستور حذف پیام خوش‌آمد (فقط در گروه)
@app.on_message(filters.command("حذف_خوشامد") & filters.group)
@adminsOnly("can_change_info")
async def delete_welcome_func(_, message):
    await del_welcome(message.chat.id)
    await message.reply_text("پیام خوش‌آمدگویی حذف شد.")

# دستور نمایش پیام خوش‌آمد (فقط در گروه)
@app.on_message(filters.command("نمایش_خوشامد") & filters.group)
@adminsOnly("can_change_info")
async def show_welcome_func(_, message):
    welcome, raw_text, file_id = await get_welcome(message.chat.id)
    if not raw_text:
        return await message.reply_text("هیچ پیام خوش‌آمدگویی تنظیم نشده است.")
    await message.reply_text(f"پیام خوش‌آمدگویی تنظیم‌شده:\n\n{raw_text}")'''
