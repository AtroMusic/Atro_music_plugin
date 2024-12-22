from pyrogram import filters
from YukkiMusic import app
import random

# لیست پیام‌های مناسب با فونت‌های خاص
robot_responses = [
    "🎶 موزیک پلیر آنلاین است 🎧",
    "🖥 ربات هم اکنون آنلاین می‌باشد 🎵",
    "💥 شاخ ربات‌ها آنلاین هست 💥",
    "🎤 جانم بگو، آنلاینم! 🎵",
    "🔊 موزیک پلیر همیشه آنلاین است!\nیک دنیای موسیقی در اختیارت هست! 🎵"
]

# دستور ربات
@app.on_message(filters.command(["ربات"], prefixes=["", "/"]) & filters.regex("^ربات$"))
async def random_robot_reply(_, message):
    # انتخاب یک پیام تصادفی از لیست
    response = random.choice(robot_responses)

    # ارسال پیام تصادفی به کاربر
    await message.reply_text(response)
