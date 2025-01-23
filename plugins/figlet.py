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

# ذخیره‌سازی متن و فونت آخرین درخواست‌ها
user_data = {}


def generate_font_list():
    """ایجاد لیستی از فونت‌های موجود."""
    fonts = pyfiglet.FigletFont.getFonts()
    buttons = [
        InlineKeyboardButton(font, callback_data=f"font_{font}")
        for font in fonts[:50]  # فقط 50 فونت برای محدودیت
    ]
    return [buttons[i : i + 3] for i in range(0, len(buttons), 3)]


def create_figlet(text, font=None):
    """ایجاد متن با فونت انتخابی یا تصادفی."""
    font = font or choice(pyfiglet.FigletFont.getFonts())
    figlet_text = str(pyfiglet.figlet_format(text, font=font))
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="تغییر فونت 🎨", callback_data="figlet"),
                InlineKeyboardButton(text="بستن ❌", callback_data="close_reply"),
            ],
            [InlineKeyboardButton(text="انتخاب فونت ➡️", callback_data="choose_font")],
        ]
    )
    return figlet_text, keyboard


@app.on_message(filters.command(["figlet","فونج"]))
async def figlet_command(bot, message):
    global user_data
    try:
        text = message.text.split(" ", 1)[1]
    except IndexError:
        return await message.reply_text("مثال:\n\n`/figlet Yukki`")
    user_data[message.from_user.id] = {"text": text}  # ذخیره متن
    figlet_text, keyboard = create_figlet(text)
    await message.reply_text(
        f"✨ متن زیبا شده شما:\n<pre>{figlet_text}</pre>",
        quote=True,
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("figlet"))
async def figlet_random_handler(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in user_data:
        return await query.answer("متن پیدا نشد، لطفاً دوباره تلاش کنید.", show_alert=True)
    text = user_data[user_id]["text"]
    figlet_text, keyboard = create_figlet(text)
    try:
        await query.message.edit_text(
            f"✨ متن زیبا شده شما:\n<pre>{figlet_text}</pre>", reply_markup=keyboard
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)


@app.on_callback_query(filters.regex("choose_font"))
async def choose_font_handler(_, query: CallbackQuery):
    font_buttons = generate_font_list()
    keyboard = InlineKeyboardMarkup(font_buttons)
    await query.message.edit_text(
        "🎨 یک فونت را انتخاب کنید:", reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("font_"))
async def specific_font_handler(_, query: CallbackQuery):
    user_id = query.from_user.id
    font_name = query.data.split("_", 1)[1]
    if user_id not in user_data:
        return await query.answer("متن پیدا نشد، لطفاً دوباره تلاش کنید.", show_alert=True)
    text = user_data[user_id]["text"]
    figlet_text, keyboard = create_figlet(text, font=font_name)
    try:
        await query.message.edit_text(
            f"✨ متن زیبا شده شما با فونت '{font_name}':\n<pre>{figlet_text}</pre>",
            reply_markup=keyboard,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)


@app.on_callback_query(filters.regex("close_reply"))
async def close_handler(_, query: CallbackQuery):
    await query.message.delete()
