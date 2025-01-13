import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TheApi import api
from YukkiMusic import app

# تابعی برای ارسال فایل به تلگراف
@app.on_message(filters.command(["تلگراف", "آپلود"]))
async def get_link_group(client, message):
    # بررسی اینکه آیا به یک پیام رسانه‌ای پاسخ داده شده است
    if not message.reply_to_message:
        return await message.reply_text(
            "لطفاً به یک رسانه پاسخ بدهید تا آن را در تلگراف آپلود کنم."
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    # بررسی اندازه فایل (نباید بیشتر از 15MB باشد)
    if file_size > 15 * 1024 * 1024:
        return await message.reply_text("لطفاً یک فایل کمتر از 15MB ارسال کنید.")

    try:
        # ارسال پیام در حال پردازش
        text = await message.reply("در حال پردازش...")

        async def progress(current, total):
            try:
                await text.edit_text(f"📥 در حال بارگیری... {current * 100 / total:.1f}%")
            except Exception:
                pass

        try:
            local_path = await media.download(progress=progress)
            await text.edit_text("📤 در حال آپلود به تلگراف...")

            # آپلود به تلگراف
            upload_path = api.upload_image(local_path)

            await text.edit_text(
                f"🌐 | [لینک آپلود شده]({upload_path})",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "دانلود فایل",
                                url=upload_path,
                            )
                        ]
                    ]
                ),
            )

            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await text.edit_text(f"❌ خطا در آپلود فایل\n\n<i>دلیل: {e}</i>")
            try:
                os.remove(local_path)
            except Exception:
                pass
            return
    except Exception:
        pass

# # راهنمای دستورات
# __HELP__ = """
# **دستورات ربات تلگراف آپلود**

# برای آپلود رسانه به تلگراف از دستورات زیر استفاده کنید:

# - ارسال به تلگراف: آپلود رسانه به تلگراف و دریافت لینک آن.
# - آپلود به تلگراف: مشابه دستور "ارسال به تلگراف".
# - تلگراف: مشابه دستور "ارسال به تلگراف".
# - آپلود: مشابه دستور "ارسال به تلگراف".

# **مثال:**
# - به یک عکس یا ویدیو پاسخ دهید و دستور "ارسال به تلگراف" را ارسال کنید تا آن را به تلگراف آپلود کنید.

# **نکته:**
# لطفاً برای آپلود، به یک فایل رسانه‌ای پاسخ دهید.
# """

# # __MODULE__ = "Tᴇʟᴇɢʀᴀᴘʜ"
