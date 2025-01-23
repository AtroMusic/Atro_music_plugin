import logging
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from YukkiMusic import app
from YukkiMusic.utils.database import (
    delete_filter,
    deleteall_filters,
    get_filter,
    get_filters_names,
    save_filter,
)
from utils.permissions import adminsOnly

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ذخیره فیلتر با دستور /filter
@app.on_message(filters.command("filter") & filters.group)
@adminsOnly("can_change_info")
async def save_filters(_, message):
    logger.info("دستور /filter دریافت شد.")
    if len(message.command) < 2 or not message.reply_to_message:
        logger.warning("دستور به درستی ارسال نشده است.")
        return await message.reply_text(
            "نحوه استفاده از دستور:\n"
            "1. به پیام موردنظر پاسخ دهید (متن، عکس، ویدیو، و غیره).\n"
            "2. دستور `/filter [نام_فیلتر]` را ارسال کنید."
        )

    filter_name = message.command[1].strip()
    reply_message = message.reply_to_message
    logger.info(f"نام فیلتر: {filter_name}")

    if reply_message.text:
        filter_data = reply_message.text
        filter_type = "text"
    elif reply_message.photo:
        filter_data = reply_message.photo.file_id
        filter_type = "photo"
    elif reply_message.video:
        filter_data = reply_message.video.file_id
        filter_type = "video"
    elif reply_message.animation:
        filter_data = reply_message.animation.file_id
        filter_type = "animation"
    elif reply_message.document:
        filter_data = reply_message.document.file_id
        filter_type = "document"
    else:
        logger.warning("نوع پیام پشتیبانی نمی‌شود.")
        return await message.reply_text("نوع پیام پشتیبانی نمی‌شود.")

    logger.info(f"ذخیره فیلتر: {filter_name}, نوع: {filter_type}")
    await save_filter(message.chat.id, filter_name, {"type": filter_type, "data": filter_data})
    await message.reply_text(f"فیلتر **{filter_name}** ذخیره شد.")

# نمایش لیست فیلترها با دستور /filters
@app.on_message(filters.command("filters") & filters.group)
async def list_filters(_, message):
    logger.info("دستور /filters دریافت شد.")
    filters_list = await get_filters_names(message.chat.id)
    if not filters_list:
        logger.info("هیچ فیلتری ذخیره نشده است.")
        return await message.reply_text("هیچ فیلتری ذخیره نشده است.")

    text = "لیست فیلترهای ذخیره‌شده:\n"
    for filter_name in filters_list:
        text += f"- {filter_name}\n"
    await message.reply_text(text)

# حذف تمامی فیلترها با دستور /stopall
@app.on_message(filters.command("stopall") & filters.group)
@adminsOnly("can_change_info")
async def remove_filters(_, message):
    logger.info("دستور /stopall دریافت شد.")
    filters_list = await get_filters_names(message.chat.id)
    if not filters_list:
        logger.info("هیچ فیلتری برای حذف وجود ندارد.")
        return await message.reply_text("هیچ فیلتری برای حذف وجود ندارد.")

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"❌ {filter_name}", callback_data=f"delete_filter:{filter_name}")]
            for filter_name in filters_list
        ]
    )
    await message.reply_text("روی دکمه فیلتر موردنظر برای حذف کلیک کنید:", reply_markup=keyboard)

# حذف فیلتر انتخاب‌شده
@app.on_callback_query(filters.regex(r"^delete_filter:(.+)"))
async def delete_filter_cb(_, query: CallbackQuery):
    logger.info("درخواست حذف فیلتر دریافت شد.")
    filter_name = query.data.split(":", 1)[1]
    chat_id = query.message.chat.id

    await delete_filter(chat_id, filter_name)
    await query.answer(f"فیلتر {filter_name} حذف شد.", show_alert=True)
    await query.message.edit_text(f"فیلتر **{filter_name}** حذف شد.")

# ارسال اطلاعات فیلتر هنگام ارسال نام
@app.on_message(filters.text & filters.group)
async def send_filter(_, message):
    logger.info("دریافت نام فیلتر.")
    filter_name = message.text.strip()
    filter_data = await get_filter(message.chat.id, filter_name)

    if not filter_data:
        logger.info("هیچ فیلتری با این نام یافت نشد.")
        return

    filter_type = filter_data["type"]
    if filter_type == "text":
        await message.reply_text(filter_data["data"])
    else:
        await message.reply_cached_media(filter_data["data"])
