import asyncio
from random import choice
import pyfiglet
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from YukkiMusic import app

# ذخیره اطلاعات کاربر
user_data = {}

# لیست ایموجی‌ها
emojis = ["✨", "🌟", "🔥", "🌈", "🎉", "💎", "⭐️", "🎵", "💖", "🌀", "❤️‍🔥"]

# ایجاد قاب‌های هنری
def create_art_frame(text):
    top_bottom = f"{choice(emojis)}" * (len(text) + 4)
    return f"{top_bottom}\n{choice(emojis)} {text} {choice(emojis)}\n{top_bottom}"


# ایجاد متن با فونت
def create_figlet(text, font=None, add_emojis=False):
    font = font or choice(pyfiglet.FigletFont.getFonts())
    figlet_text = str(pyfiglet.figlet_format(text, font=font))
    if add_emojis:
        figlet_text = create_art_frame(figlet_text)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🎨 تغییر فونت", callback_data="figlet"),
                InlineKeyboardButton(text="❌ بستن", callback_data="close_reply"),
            ],
            [InlineKeyboardButton(text="🔤 انتخاب فونت", callback_data="choose_font")],
        ]
    )
    return figlet_text, keyboard


# لیست فونت‌ها
def generate_font_list():
    fonts = pyfiglet.FigletFont.getFonts()
    buttons = [
        InlineKeyboardButton(font, callback_data=f"font_{font}")
        for font in fonts[:30]  # فقط 30 فونت
    ]
    return [buttons[i : i + 3] for i in range(0, len(buttons), 3)]


# پاسخ به کلمه کلیدی "فونت"
@app.on_message(filters.text & (filters.private | filters.group))
async def figlet_command(bot, message):
    global user_data
    if not message.text.startswith("فونج"):
        return  # فقط پیام‌هایی که با "فونت" شروع می‌شوند

    try:
        text = message.text.split(" ", 1)[1]
    except IndexError:
        return await message.reply_text("📝 لطفاً متنی را پس از کلمه 'فونت' وارد کنید.\nمثال:\n\n`فونت سلام`")
    
    user_data[message.from_user.id] = {"text": text}
    figlet_text, keyboard = create_figlet(text, add_emojis=True)
    await message.reply_text(
        f"✨ متن زیبا شده شما:\n<pre>{figlet_text}</pre>",
        quote=True,
        reply_markup=keyboard,
    )


# تغییر فونت تصادفی
@app.on_callback_query(filters.regex("figlet"))
async def figlet_random_handler(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in user_data:
        return await query.answer("❌ متن پیدا نشد، لطفاً دوباره تلاش کنید.", show_alert=True)
    text = user_data[user_id]["text"]
    figlet_text, keyboard = create_figlet(text, add_emojis=True)
    try:
        await query.message.edit_text(
            f"✨ متن زیبا شده شما:\n<pre>{figlet_text}</pre>", reply_markup=keyboard
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)


# انتخاب فونت خاص
@app.on_callback_query(filters.regex("choose_font"))
async def choose_font_handler(_, query: CallbackQuery):
    font_buttons = generate_font_list()
    keyboard = InlineKeyboardMarkup(font_buttons)
    await query.message.edit_text(
        "🔤 یک فونت را انتخاب کنید:", reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("font_"))
async def specific_font_handler(_, query: CallbackQuery):
    user_id = query.from_user.id
    font_name = query.data.split("_", 1)[1]
    if user_id not in user_data:
        return await query.answer("❌ متن پیدا نشد، لطفاً دوباره تلاش کنید.", show_alert=True)
    text = user_data[user_id]["text"]
    figlet_text, keyboard = create_figlet(text, font=font_name, add_emojis=True)
    try:
        await query.message.edit_text(
            f"✨ متن زیبا شده شما با فونت '{font_name}':\n<pre>{figlet_text}</pre>",
            reply_markup=keyboard,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)


# بستن پیام
@app.on_callback_query(filters.regex("close_reply"))
async def close_handler(_, query: CallbackQuery):
    await query.message.delete()

