import datetime
import re

from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app
from YukkiMusic.utils.database import (
    deleteall_filters,
    get_filter,
    get_filters_names,
    save_filter,
)
from YukkiMusic.utils.functions import (
    check_format,
    extract_text_and_keyb,
    get_data_and_name,
)
from YukkiMusic.utils.keyboard import ikb

from utils.error import capture_err
from utils.permissions import adminsOnly, member_permissions


# توضیحات: این کد برای مدیریت فیلترهای گروه طراحی شده است. فقط مدیران و سازنده گروه می‌توانند از دستورات استفاده کنند.


# دستور: ایجاد فیلتر
@app.on_message(filters.command("filter") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")  # فقط مدیرانی که مجوز تغییر اطلاعات گروه دارند می‌توانند از این دستور استفاده کنند.
async def save_filters(_, message):
    try:
        # اگر دستور بدون نام فیلتر وارد شود، خطا می‌دهد.
        if len(message.command) < 2:
            return await message.reply_text(
                "**نحوه استفاده:**\nبرای ایجاد فیلتر، به یک پیام پاسخ داده و از دستور `/filter [نام_فیلتر]` استفاده کنید."
            )

        # دریافت پیام ریپلای‌شده
        replied_message = message.reply_to_message
        if not replied_message:
            replied_message = message
        data, name = await get_data_and_name(replied_message, message)

        # بررسی طول نام فیلتر
        if len(name) < 2:
            return await message.reply_text("نام فیلتر باید حداقل ۲ کاراکتر باشد.")

        if data == "error":
            return await message.reply_text(
                "**نحوه استفاده:**\n`/filter [نام_فیلتر] [محتوا]`\nیا به یک پیام پاسخ دهید و دستور `/filter [نام_فیلتر]` را وارد کنید."
            )

        # شناسایی نوع پیام ریپلای‌شده
        if replied_message.text:
            _type = "text"
            file_id = None
        elif replied_message.sticker:
            _type = "sticker"
            file_id = replied_message.sticker.file_id
        elif replied_message.animation:
            _type = "animation"
            file_id = replied_message.animation.file_id
        elif replied_message.photo:
            _type = "photo"
            file_id = replied_message.photo.file_id
        elif replied_message.document:
            _type = "document"
            file_id = replied_message.document.file_id
        elif replied_message.video:
            _type = "video"
            file_id = replied_message.video.file_id
        elif replied_message.video_note:
            _type = "video_note"
            file_id = replied_message.video_note.file_id
        elif replied_message.audio:
            _type = "audio"
            file_id = replied_message.audio.file_id
        elif replied_message.voice:
            _type = "voice"
            file_id = replied_message.voice.file_id
        else:
            return await message.reply_text("نوع پیام پشتیبانی نمی‌شود.")

        # ذخیره اطلاعات فیلتر
        name = name.replace("_", " ")
        _filter = {
            "type": _type,
            "data": data,
            "file_id": file_id,
        }
        chat_id = message.chat.id
        await save_filter(chat_id, name, _filter)

        return await message.reply_text(f"فیلتر **{name}** با موفقیت ذخیره شد.")
    except UnboundLocalError:
        return await message.reply_text("پیام پاسخ داده‌شده قابل دسترسی نیست. لطفاً پیام را فوروارد کنید و دوباره تلاش کنید.")


# دستور: مشاهده لیست فیلترها
@app.on_message(filters.command(["filters", "فیلتیر"]) & ~filters.private & ~BANNED_USERS)
@capture_err
async def get_filterss(_, message):
    _filters = await get_filters_names(message.chat.id)
    if not _filters:
        return await message.reply_text("هیچ فیلتری در این گروه ذخیره نشده است.")
    _filters.sort()
    msg = f"لیست فیلترهای ذخیره‌شده در گروه **{message.chat.title}** :\n"
    for _filter in _filters:
        msg += f"- {str(_filter)}\n"
    await message.reply_text(msg)


# حذف همه فیلترها
@app.on_message(filters.command("stopall") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def stop_all(_, message):
    _filters = await get_filters_names(message.chat.id)
    if not _filters:
        return await message.reply_text("هیچ فیلتری در این گروه ذخیره نشده است.")
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("بله، حذف کن", callback_data="stop_yes"),
                    InlineKeyboardButton("نه، منصرف شدم", callback_data="stop_no"),
                ]
            ]
        )
        await message.reply_text(
            "آیا مطمئن هستید که می‌خواهید تمام فیلترهای این گروه را حذف کنید؟",
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("stop_(.*)") & ~BANNED_USERS)
async def stop_all_cb(_, cb):
    chat_id = cb.message.chat.id
    from_user = cb.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    if "can_change_info" not in permissions:
        return await cb.answer("شما مجوز لازم برای این عملیات را ندارید.", show_alert=True)
    input = cb.data.split("_", 1)[1]
    if input == "yes":
        await deleteall_filters(chat_id)
        await cb.message.edit("تمام فیلترهای این گروه با موفقیت حذف شدند.")
    elif input == "no":
        await cb.message.delete()

