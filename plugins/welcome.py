import datetime
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import (
    Chat,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from YukkiMusic import app
from utils.database import set_welcome, get_welcome, del_welcome


async def send_welcome_message(chat: Chat, user):
    """ارسال پیام خوش‌آمدگویی برای کاربر جدید."""
    welcome_data = await get_welcome(chat.id)
    if not welcome_data:
        return

    raw_text, file_id = welcome_data
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    text = raw_text.replace("{USER}", user.mention).replace("{DATE}", date)

    await app.send_message(
        chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("پروفایل کاربر", url=f"tg://user?id={user.id}")]]
        ),
    )


async def send_goodbye_message(user, chat_title, group_link):
    """ارسال پیام خداحافظی به پیوی کاربر."""
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    text = (
        f"👋 خداحافظ {user.mention}!\n"
        f"شما از گروه {chat_title} خارج شدید.\n"
        f"ما از خروج شما متأسفیم و امیدواریم دوباره بازگردید.\n"
        f"⏰ تاریخ خروج شما: {date}\n\n"
        f"برای بازگشت به گروه، می‌توانید از دکمه زیر استفاده کنید:"
    )

    try:
        await app.send_message(
            chat_id=user.id,
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔗 بازگشت به گروه", url=group_link)]]
            ),
        )
    except Exception:
        pass


@app.on_chat_member_updated(filters.group)
async def member_update(_, chat_member: ChatMemberUpdated):
    """مدیریت ورود و خروج کاربران."""
    if chat_member.new_chat_member.status == CMS.MEMBER:
        user = chat_member.new_chat_member.user
        chat = chat_member.chat
        await send_welcome_message(chat, user)

    elif chat_member.old_chat_member and chat_member.new_chat_member.status in {
        CMS.LEFT,
        CMS.BANNED,
    }:
        user = chat_member.old_chat_member.user
        chat = chat_member.chat
        group_link = f"https://t.me/{chat.username}" if chat.username else "لینک خصوصی تنظیم نشده است."
        await send_goodbye_message(user, chat.title, group_link)


@app.on_message(filters.command("تنظیم_خوشامد") & filters.group)
async def set_welcome_message(_, message):
    """تنظیم پیام خوش‌آمدگویی."""
    if not message.reply_to_message:
        await message.reply_text("لطفاً به یک پیام ریپلای کنید تا به عنوان خوش‌آمد تنظیم شود.")
        return

    raw_text = message.reply_to_message.text
    if not raw_text:
        await message.reply_text("پیام ریپلای‌شده باید شامل متن باشد.")
        return

    await set_welcome(message.chat.id, raw_text, None)
    await message.reply_text("✅ پیام خوش‌آمد با موفقیت تنظیم شد.")


@app.on_message(filters.command("حذف_خوشامد") & filters.group)
async def delete_welcome_message(_, message):
    """حذف پیام خوش‌آمدگویی."""
    await del_welcome(message.chat.id)
    await message.reply_text("✅ پیام خوش‌آمد با موفقیت حذف شد.")


@app.on_message(filters.command("خوشامد_وضعیت") & filters.group)
async def get_welcome_status(_, message):
    """نمایش وضعیت پیام خوش‌آمدگویی."""
    welcome_data = await get_welcome(message.chat.id)
    if not welcome_data:
        await message.reply_text("❌ پیام خوش‌آمد تنظیم نشده است.")
    else:
        raw_text, file_id = welcome_data
        await message.reply_text(f"✅ پیام خوش‌آمد فعال است:\n\n{raw_text}")
