import os
import random
import requests
from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TheApi import api
from YukkiMusic import app
from utils import get_couple, get_image, save_couple

# لیست اشعار عاشقانه
poems = [
    "تو تنها دلیل زندگی منی ❤️",
    "تا دنیا دنیاست، دل من با دل تو یکی است 💕",
    "با عشق تو دنیا برایم زیباتر است 🌹",
    "هر لحظه با تو، لحظه‌ای از بهشت است ✨",
    "عشق ما ابدی است، مانند خورشید و ماه 🌙☀️",
    "با تو بودن یعنی آرامش جان و دل 💖",
    "تو زیباترین اتفاق زندگی منی 💘",
    "به تو که فکر می‌کنم، دلم پر از شادی می‌شود 🌷",
    "با تو عشق را در تک‌تک لحظه‌ها حس می‌کنم 💞",
    "قلبم برای تو می‌تپد، همیشه و تا ابد ❤️",
    "تو روشنی قلب تاریک منی 🌟",
    "هر بار که به تو نگاه می‌کنم، دوباره عاشق می‌شوم 💓",
    "عشق تو دنیای مرا رنگین‌تر کرده است 🌈",
    "بی‌تو، دنیا برایم چیزی جز سکوت نیست 💔",
    "هر لحظه کنار تو یعنی خوشبختی 🍀",
    "با تو هر راهی به سوی بهشت می‌رود 🌺",
    "تو شعله‌ای هستی که زندگی‌ام را گرم می‌کند 🔥",
    "عشق تو دلیل تمام لبخندهای من است 😊",
    "تو ستاره‌ی روشن شب‌های منی 🌌",
    "هر روزی که با تو می‌گذرد، بهترین روز زندگی من است 🌷",
    "عشق تو مثل نسیمی است که روح مرا تازه می‌کند 💨",
    "تو رویای شیرین شب‌های منی 🌙",
    "در نگاه تو آرامشی است که هیچ‌جا پیدا نمی‌کنم 💖",
    "دنیای من با تو کامل می‌شود 🌟",
    "تو آهنگ دلنشین زندگی منی 🎵",
    "با تو هر ثانیه زیباترین لحظه است ⏳",
    "تو همان عشقی هستی که همیشه آرزویش را داشتم 💕",
    "کنار تو همه چیز ممکن است 🌟",
    "قلب من تا همیشه برای تو خواهد تپید ❤️",
]

# دانلود تصویر از آدرس URL
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path

@app.on_message(filters.text & filters.group)
async def couple_handler(_, message):
    if not message.text.startswith("زوج"):
        return

    cid = message.chat.id
    args = message.text.split()
    p1_path = "downloads/pfp.png"
    p2_path = "downloads/pfp1.png"
    test_image_path = f"downloads/test_{cid}.png"
    cppic_path = "downloads/cppic.png"

    try:
        # انتخاب تصادفی زوج در صورت عدم وجود آرگومان
        if len(args) == 1:
            list_of_users = [
                member.user.id
                async for member in app.get_chat_members(message.chat.id, limit=50)
                if not member.user.is_bot and not member.user.is_deleted
            ]

            if len(list_of_users) < 2:
                return await message.reply_text("تعداد کاربران کافی برای انتخاب زوج وجود ندارد.")

            c1_id = random.choice(list_of_users)
            c2_id = random.choice([u for u in list_of_users if u != c1_id])

        # انتخاب زوج مشخص در صورت وجود شناسه یا یوزرنیم
        elif len(args) == 3:
            try:
                c1 = await app.get_users(args[1])
                c2 = await app.get_users(args[2])
                c1_id, c2_id = c1.id, c2.id
            except Exception:
                return await message.reply_text("❌ یکی از شناسه‌ها یا یوزرنیم‌ها اشتباه است.")

        else:
            return await message.reply_text("❌ دستور نادرست است. لطفاً دستور را به شکل صحیح ارسال کنید.")

        # دریافت تصاویر پروفایل کاربران
        photo1 = (await app.get_chat(c1_id)).photo
        photo2 = (await app.get_chat(c2_id)).photo
        c1_name = (await app.get_users(c1_id)).mention
        c2_name = (await app.get_users(c2_id)).mention

        try:
            p1 = await app.download_media(photo1.big_file_id, file_name=p1_path)
        except Exception:
            p1 = download_image(
                "https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p1_path
            )
        try:
            p2 = await app.download_media(photo2.big_file_id, file_name=p2_path)
        except Exception:
            p2 = download_image(
                "https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p2_path
            )
        img1 = Image.open(p1).resize((437, 437))
        img2 = Image.open(p2).resize((437, 437))
        mask = Image.new("L", img1.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + img1.size, fill=255)

        mask1 = Image.new("L", img2.size, 0)
        ImageDraw.Draw(mask1).ellipse((0, 0) + img2.size, fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask1)

        background_image_path = download_image(
            "https://telegra.ph/file/96f36504f149e5680741a.jpg", cppic_path
        )
        img = Image.open(background_image_path)
        img.paste(img1, (116, 160), img1)
        img.paste(img2, (789, 160), img2)

        img.save(test_image_path)

        # انتخاب شعر عاشقانه تصادفی
        poem = random.choice(poems)

        # ارسال پیام با کلید شیشه‌ای
        caption = f"""
✨ زوج امروز:

{c1_name} ❤️ {c2_name}

📜 شعر عاشقانه:
"{poem}"
        """
        await message.reply_photo(
            test_image_path,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="✨ افزودن من به گروه", url=f"https://t.me/{app.username}?startgroup=true"
                        )
                    ]
                ]
            ),
        )

        # آپلود تصویر و ذخیره داده‌ها
        img_url = api.upload_image(test_image_path)
        couple = {"c1_id": c1_id, "c2_id": c2_id}
        await save_couple(cid, "", couple, img_url)

    except Exception as e:
        await message.reply_text(f"❌ خطایی رخ داده است: {e}")
