𝙎꯭𝘼꯭𝘿꯭𝙀꯭𝙌꯭➤︎︎꯭⃝꯭𓃮꯭𝗔꯭𝗧꯭𝗥꯭𝗢꯭, [1/5/2025 10:03 AM]
import datetime
from re import findall

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import (
    Chat,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import is_gbanned_user
from YukkiMusic.utils.functions import check_format, extract_text_and_keyb
from YukkiMusic.utils.keyboard import ikb

from utils import del_welcome, get_welcome, set_welcome
from utils.error import capture_err
from utils.permissions import adminsOnly

from .notes import extract_urls


# مدیریت کاربر جدید
async def handle_new_member(member, chat):
    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} به دلیل مسدودیت جهانی از گروه حذف شد. "
                "برای درخواست رفع مسدودیت، لطفاً با پشتیبانی تماس بگیرید.",
            )
            return
        if member.is_bot:
            return
        return await send_welcome_message(chat, member.id)
    except ChatAdminRequired:
        return


# مدیریت لفت‌بک (بازگشت کاربر به گروه)
@app.on_chat_member_updated(filters.group, group=6)
@capture_err
async def welcome_and_left(_, user: ChatMemberUpdated):
    # خوش‌آمدگویی به کاربران جدید
    if user.new_chat_member and user.new_chat_member.status not in {CMS.RESTRICTED}:
        member = user.new_chat_member.user if user.new_chat_member else user.from_user
        chat = user.chat
        return await handle_new_member(member, chat)
    
    # شناسایی خروج کاربران
    if user.old_chat_member and user.old_chat_member.status == CMS.MEMBER:
        if user.new_chat_member and user.new_chat_member.status == CMS.LEFT:
            chat = user.chat
            member = user.old_chat_member.user
            try:
                group_link = await app.create_chat_invite_link(chat.id)
                await app.send_message(
                    member.id,
                    f"سلام {member.first_name}!\n"
                    "شما از گروه {chat.title} خارج شده‌اید.\n"
                    "برای بازگشت به گروه، روی دکمه زیر کلیک کنید:",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("بازگشت به گروه", url=group_link.invite_link)]
                        ]
                    ),
                )
            except Exception as e:
                print(f"Error sending message to {member.id}: {e}")
            return


# ارسال پیام خوش‌آمدگویی
async def send_welcome_message(chat: Chat, user_id: int, delete: bool = False):
    welcome, raw_text, file_id = await get_welcome(chat.id)
    if not raw_text:
        return
    text = raw_text
    keyb = None
    if findall(r".+\,.+", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)
    u = await app.get_users(user_id)
    text = text.replace("{GROUPNAME}", chat.title)
    text = text.replace("{NAME}", u.mention)
    text = text.replace("{ID}", f"{user_id}")
    text = text.replace("{FIRSTNAME}", u.first_name)
    text = text.replace("{SURNAME}", u.last_name or "نامشخص")
    text = text.replace("{USERNAME}", u.username or "نامشخص")
    text = text.replace("{DATE}", datetime.datetime.now().strftime("%Y-%m-%d"))
    text = text.replace("{WEEKDAY}", datetime.datetime.now().strftime("%A"))
    text = text.replace("{TIME}", datetime.datetime.now().strftime("%H:%M:%S UTC"))
    
    if welcome == "Text":
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,)
    elif welcome == "Photo":
        m = await app.send_photo(
            chat.id,
            photo=file_id,
            caption=text,
            reply_markup=keyb,
        )
    else:
        m = await app.send_animation(
            chat.id,
            animation=file_id,
            caption=text,
            reply_markup=keyb,
        )


# دستورات فارسی
@app.on_message(filters.command("تنظیم_خوشامد") & ~filters.private)
@adminsOnly("can_change_info")
async def set_welcome_func(_, message):
    usage = "لطفاً به یک متن، عکس یا GIF پاسخ دهید تا به‌عنوان پیام خوش‌آمدگویی تنظیم شود."
    replied_message = message.reply_to_message
    chat_id = message.chat.id
    if not replied_message:
        return await message.reply_text(usage)
    
    if replied_message.animation:
        welcome = "Animation"
        file_id = replied_message.animation.file_id
        text = replied_message.caption
    elif replied_message.photo:
        welcome = "Photo"
        file_id = replied_message.photo.file_id
        text = replied_message.caption
    else:
        welcome = "Text"
        file_id = None
        text = replied_message.text
    
    raw_text = await check_format(ikb, text.markdown if text else "")
    await set_welcome(chat_id, welcome, raw_text, file_id)
    await message.reply_text("پیام خوش‌آمدگویی با موفقیت تنظیم شد.")


@app.on_message(filters.command(["حذف_خوشامد", "delwelcome"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_welcome_func(_, message):
    chat_id = message.chat.id
    await del_welcome(chat_id)
    await message.reply_text("پیام خوش‌آمدگویی حذف شد.")


@app.on_message(filters.command("نمایش_خوشامد") & ~filters.private)
@adminsOnly("can_change_info")
async def get_welcome_func(_, message):
    chat = message.chat
    welcome, raw_text, file_id = await get_welcome(chat.id)
    if not raw_text:
        return await message.reply_text("هیچ پیام خوش‌آمدگویی تنظیم نشده است.")
    await send_welcome_message(chat, message.from_user.id)
