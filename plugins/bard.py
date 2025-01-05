import random
from pyrogram import filters
from YukkiMusic import app

# فرمان عشق
@app.on_message(filters.command(["love", "عشق", "کراشم"], prefixes=["", "/"]) & filters.group)
async def love_command(client, message):
    args = message.text.split()[1:]  # حذف فرمان و دریافت آرگومان‌ها

    # چک کردن وارد شدن دقیقاً دو آرگومان
    if len(args) != 2:
        await message.delete()  # هیچ پاسخی نمی‌دهد
        return

    name1 = args[0].strip()
    name2 = args[1].strip()

    # بررسی صحت یوزرنیم یا آی‌دی عددی
    if not (is_valid_username_or_id(name1) and is_valid_username_or_id(name2)):
        await message.delete()  # هیچ پاسخی نمی‌دهد
        return

    # دریافت اطلاعات کاربران
    try:
        user1 = await client.get_users(name1)
        user2 = await client.get_users(name2)
    except:
        await message.delete()  # اگر کاربر نامعتبر باشد، پاسخی نمی‌دهد
        return

    # محاسبه درصد عشق
    love_percentage = random.randint(10, 100)
    love_message = get_random_message(love_percentage)

    # انتخاب ایموجی تصادفی
    love_emoji = random.choice(["❤️", "💖", "💞", "💘", "💕", "🌹", "💑", "🔥", "✨"])

    # ساخت پاسخ
    response = f"""
{love_emoji} {user1.mention} ❤️ {user2.mention} {love_emoji}

📊 درصد عشق شما: {love_percentage}%

💌 پیام ویژه:  
{love_message}

✨ باور داشته باشید که عشق همیشه راهی پیدا می‌کند! 🌟
"""
    # ارسال پاسخ و حذف پیام کاربر
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

# بررسی صحت یوزرنیم یا آی‌دی عددی
def is_valid_username_or_id(value):
    # بررسی آی‌دی عددی
    if value.isdigit():
        return True
    # بررسی یوزرنیم
    if value.startswith("@") and len(value) > 1:
        return True
    return False
