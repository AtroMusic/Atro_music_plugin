import random
from pyrogram import filters
from YukkiMusic import app

# فرمان عشق
@app.on_message(filters.command(["love", "عشق", "کراشم"], prefixes=["", "/"]))
async def love_command(client, message):
    args = message.text.split()[1:]  # حذف فرمان و دریافت آرگومان‌ها
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        # محاسبه درصد عشق
        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        # انتخاب یک ایموجی تصادفی برای جذابیت بیشتر
        love_emoji = random.choice(["❤️", "💖", "💞", "💘", "💕", "🌹", "💑", "🔥", "✨"])

        # ساخت پاسخ
        response = f"""
{love_emoji} {name1} ❤️ {name2} {love_emoji}

📊 درصد عشق شما: {love_percentage}%

💌 پیام ویژه:  
{love_message}

✨ باور داشته باشید که عشق همیشه راهی پیدا می‌کند! 🌟
"""
        # ارسال پاسخ و حذف پیام کاربر
        await client.send_message(chat_id=message.chat.id, text=response)
        await message.delete()
    else:
        # پیام خطا در صورت وارد نکردن دو نام
        response = "❗ لطفاً بعد از دستور /love دو نام وارد کنید."
        await client.send_message(chat_id=message.chat.id, text=response)
        await message.delete()

# تولید پیام‌های تصادفی عاشقانه بر اساس درصد
def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "💔 عشق شما هنوز نیاز به صبر و تلاش دارد، اما ناامید نشوید.",
                "🌱 یک شروع کوچک، اما هر عشقی از همین‌جا آغاز می‌شود.",
                "✨ با کمی مراقبت و توجه، شاید این رابطه شکوفا شود.",
                "🧡 هنوز به جرقه‌ای نیاز دارید تا آتش عشق روشن شود.",
            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "💓 یک پیوند محکم در حال شکل‌گیری است. ادامه دهید!",
                "💖 عشق میان شما در حال رشد است، آن را گرامی بدارید.",
                "🌟 شانس خوبی برای خوشبختی دارید. از آن استفاده کنید.",
                "💫 داستان عاشقانه شما در مسیر زیبایی پیش می‌رود.",
            ]
        )
    else:
        return random.choice(
            [
                "💞 عشق شما یک افسانه است! هر لحظه آن را جشن بگیرید.",
                "💍 این یک پیوند آسمانی است! شما برای هم ساخته شده‌اید.",
                "❤️ سرنوشت شما را به هم رسانده است. تبریک می‌گویم!",
                "🌹 عشق شما بی‌پایان و بی‌نظیر است. قدرش را بدانید.",
            ]
        )

# یادداشت: کد بالا تضمین می‌کند که پیام‌ها زیبا و جذاب باشند، 
# پیام کاربر حذف شود و پاسخ دلنشین‌تر از قبل باشد.
