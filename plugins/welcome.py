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

async def handle_new_member(member, chat):
    """مدیریت کاربران جدید گروه."""
    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"❌ کاربر {member.mention} به دلیل ممنوعیت سراسری از گروه حذف شد."
            )
            return
        if member.is_bot:
            return
        await send_welcome_message(chat, member.id)
    except ChatAdminRequired:
        return

async def handle_left_member(member, chat):
    """مدیریت خروج یا حذف کاربران از گروه."""
    try:
        if member.is_bot:
            return
        await send_goodbye_message(chat, member.id)
        await send_private_message(member)
    except ChatAdminRequired:
        return

@app.on_chat_member_updated(filters.group, group=6)
@capture_err
async def welcome_goodbye_handler(_, user: ChatMemberUpdated):
    """مدیریت رویداد ورود یا خروج کاربران."""
    if user.new_chat_member:
        return await handle_new_member(user.new_chat_member.user, user.chat)
    if user.old_chat_member and user.old_chat_member.status == CMS.LEFT:
        return await handle_left_member(user.old_chat_member.user, user.chat)

async def send_welcome_message(chat: Chat, user_id: int):
    """ارسال پیام خوش‌آمدگویی به گروه."""
    welcome, raw_text, file_id = await get_welcome(chat.id)
    if not raw_text:
        return
    text, keyb = await process_message(chat, user_id, raw_text)
    text += f"\n\n📅 تاریخ عضویت: {datetime.datetime.now().strftime('%Y-%m-%d')}"
    await send_message(chat, text, file_id, keyb, welcome)

async def send_goodbye_message(chat: Chat, user_id: int):
    """ارسال پیام خداحافظی به گروه."""
    goodbye_message = f"❌ کاربر {user_id} گروه را ترک کرد. امیدواریم دوباره شما را ببینیم!"
    await app.send_message(chat.id, goodbye_message)

async def send_private_message(member):
    """ارسال پیام خصوصی به کاربر هنگام خروج."""
    try:
        goodbye_message = (
            f"سلام {member.mention}،\n"
            "متأسفیم که گروه را ترک کردید. اگر می‌خواهید دوباره عضو شوید، از لینک زیر استفاده کنید: 👇"
        )
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔗 بازگشت به گروه", url="https://t.me/YourGroupLink")]]
        )
        await app.send_message(
            member.id,
            goodbye_message,
            reply_markup=keyboard
        )
    except Exception:
        print(f"❌ ارسال پیام به {member.id} انجام نشد.")

async def process_message(chat: Chat, user_id: int, raw_text: str):
    """جایگزینی متن پیام‌ها با اطلاعات واقعی."""
    u = await app.get_users(user_id)
    text = raw_text.replace("{GROUPNAME}", chat.title)
    text = text.replace("{NAME}", u.mention)
    text = text.replace("{ID}", str(user_id))
    text = text.replace("{FIRSTNAME}", u.first_name)
    text = text.replace("{SURNAME}", u.last_name or "ندارد")
    text = text.replace("{USERNAME}", u.username or "ندارد")
    text = text.replace("{DATE}", datetime.datetime.now().strftime("%Y-%m-%d"))
    text = text.replace("{TIME}", datetime.datetime.now().strftime("%H:%M:%S"))
    keyb = None
    if findall(r".+\,.+", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)
        return text, keyb
    async def send_message(chat: Chat, text: str, file_id: str, keyb, message_type: str):
        """ارسال پیام خوش‌آمدگویی یا خداحافظی."""
    if message_type == "Text":
        await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    elif message_type == "Photo":
        await app.send_photo(
            chat.id,
            photo=file_id,
            caption=text,
            reply_markup=keyb,
        )
    elif message_type == "Animation":
        await app.send_animation(
            chat.id,
            animation=file_id,
            caption=text,
            reply_markup=keyb,
        )

@app.on_message(filters.command("setwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def set_welcome_func(_, message):
    """تنظیم پیام خوش‌آمدگویی."""
    usage = "شما باید به یک متن، عکس یا GIF پاسخ دهید تا آن را به عنوان پیام خوش‌آمدگویی تنظیم کنید."
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
    elif replied_message.text:
        welcome = "Text"
        file_id = None
        text = replied_message.text
    else:
        return await message.reply_text(usage)
    raw_text = await check_format(ikb, text)
    await set_welcome(chat_id, welcome, raw_text, file_id)
    await message.reply_text("پیام خوش‌آمدگویی با موفقیت تنظیم شد.")

@app.on_message(filters.command(["delwelcome", "deletewelcome"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_welcome_func(_, message):
    """حذف پیام خوش‌آمدگویی."""
    await del_welcome(message.chat.id)
    await message.reply_text("پیام خوش‌آمدگویی حذف شد.")

@app.on_message(filters.command("getwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def get_welcome_func(_, message):
    """مشاهده پیام خوش‌آمدگویی فعلی."""
    welcome, raw_text, file_id = await get_welcome(message.chat.id)
    if not raw_text:
        return await message.reply_text("پیام خوش‌آمدگویی تنظیم نشده است.")
    await message.reply_text(f"پیام خوش‌آمدگویی:\n\n{raw_text}")
