from os import remove
from pyrogram import filters
from lexica import Client as LexicaClient
from pyrogram.errors.exceptions.bad_request_400 import PhotoInvalidDimensions
from YukkiMusic import app
from utils.error import capture_err
from PIL import Image
import logging
import json

# تنظیمات اولیه
lexica_client = LexicaClient()
logging.basicConfig(filename='errors.log', level=logging.ERROR)
LANGUAGES = {
    "fa": {
        "start": "✨ شروع پردازش تصویر...",
        "done": "✅ تصویر با موفقیت ارتقا یافت!",
        "error": "❌ خطا در پردازش تصویر.",
        "not_photo": "⚠️ لطفاً به یک عکس پاسخ دهید!",
        "almost_done": "🚀 تصویر در حال ارتقا است...",
        "saved": "✅ تصویر ذخیره شد!",
        "deleted": "🗑️ تصویر حذف شد."
    },
    "en": {
        "start": "✨ Starting image processing...",
        "done": "✅ Image upscale completed!",
        "error": "❌ Error in image processing.",
        "not_photo": "⚠️ Please reply to a photo!",
        "almost_done": "🚀 Upscaling image...",
        "saved": "✅ Image saved!",
        "deleted": "🗑️ Image deleted."
    }
}
lang = "fa"  # زبان پیش‌فرض

# ذخیره تاریخچه تصاویر
def save_history(user_id, image_path):
    history = {}
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        pass
    history[str(user_id)] = history.get(str(user_id), []) + [image_path]
    with open("history.json", "w") as f:
        json.dump(history, f)

# بهبود کیفیت تصویر
def upscale_image(image: bytes, factor: int = 4) -> bytes:
    return lexica_client.upscale(image, factor)

# فشرده‌سازی تصویر
def compress_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, format="JPEG", quality=quality)

@app.on_message(filters.command("upscale"))
@capture_err
async def upscale_reply_image(client, message):
    args = message.text.split()
    level = "medium"
    if len(args) > 1:
        level = args[1].lower()
    upscale_factor = {"low": 2, "medium": 4, "high": 8}.get(level, 4)

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text(LANGUAGES[lang]["not_photo"])

    await message.reply_text(LANGUAGES[lang]["start"])
    a = await message.reply_text(LANGUAGES[lang]["almost_done"])

    photo = await client.download_media(message.reply_to_message.photo.file_id)

    with open(photo, 'rb') as f:
        image_bytes = f.read()

    try:
        upscaled_image_bytes = upscale_image(image_bytes, upscale_factor)
        with open('upscaled.png', 'wb') as f:
            f.write(upscaled_image_bytes)

        compress_image('upscaled.png', 'upscaled_compressed.jpg')

        preview_message = await message.reply_photo(photo='upscaled_compressed.jpg', caption="این پیش‌نمایش تصویر است. آیا ذخیره شود؟ (بله/خیر)")
        reply = await app.listen(preview_message.chat.id)

        if reply.text.lower() == "بله":
            await message.reply_photo(photo='upscaled_compressed.jpg', caption=LANGUAGES[lang]["done"])
            save_history(message.from_user.id, 'upscaled_compressed.jpg')
        else:
            await message.reply_text(LANGUAGES[lang]["deleted"])

        remove('upscaled.png')
        remove('upscaled_compressed.jpg')
        await a.delete()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await a.edit(LANGUAGES[lang]["error"])
        remove('upscaled.png')
