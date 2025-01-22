import datetime
import re

from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app
from YukkiMusic.utils.database import (
    delete_chat,  # برای حذف چت ذخیره‌شده
    get_saved_chats,  # برای گرفتن چت‌های ذخیره‌شده
    save_chat,  # برای ذخیره چت جدید
)
from utils.permissions import adminsOnly



@app.on_message(filters.command("تنظیم چت") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def set_chat(_, message):
    try:
        if len(message.command) < 2:
            return await message.reply_text("**استفاده:** تنظیم چت [نام چت] [محتوا]")

        chat_name = message.command[1]  # گرفتن اسم چت از دستور
        replied_message = message.reply_to_message

        if not replied_message:
            return await message.reply_text("لطفا به یک پیام ریپلای کنید تا اطلاعات چت ذخیره شود.")
        
        data = None
        file_id = None
        _type = None
        
        # تشخیص نوع داده و ذخیره آن
        if replied_message.text:
            _type = "text"
            data = replied_message.text
        elif replied_message.sticker:
            _type = "sticker"
            file_id = replied_message.sticker.file_id
        elif replied_message.animation:
            _type = "animation"
            file_id = replied_message.animation.file_id
        elif replied_message.photo:
            _type = "photo"
            file_id = replied_message.photo.file_id
        elif replied_message.video:
            _type = "video"
            file_id = replied_message.video.file_id
        elif replied_message.audio:
            _type = "audio"
            file_id = replied_message.audio.file_id
        
        if not data and not file_id:
            return await message.reply_text("فقط متن، رسانه و فایل‌ها پشتیبانی می‌شوند.")

        chat_data = {
            "type": _type,
            "data": data,
            "file_id": file_id,
        }

        await save_chat(message.chat.id, chat_name, chat_data)
        return await message.reply_text(f"اطلاعات چت برای '{chat_name}' ذخیره شد.")
    
    except Exception as e:
        return await message.reply_text(f"خطا: {str(e)}")

@app.on_message(filters.command("حذف چت") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def remove_chat(_, message):
    try:
        if len(message.command) < 2:
            return await message.reply_text("**استفاده:** حذف چت [نام چت]")
        
        chat_name = message.command[1]
        removed = await delete_chat(message.chat.id, chat_name)
        
        if removed:
            return await message.reply_text(f"چت '{chat_name}' حذف شد.")
        else:
            return await message.reply_text(f"چت '{chat_name}' پیدا نشد.")
    
    except Exception as e:
        return await message.reply_text(f"خطا: {str(e)}")

@app.on_message(filters.command("لیست چت‌ها") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def list_chats(_, message):
    try:
        saved_chats = await get_saved_chats(message.chat.id)
        if not saved_chats:
            return await message.reply_text("هیچ چتی ذخیره نشده است.")
        
        msg = "چت‌های ذخیره‌شده:\n"
        for chat_name in saved_chats:
            msg += f"- {chat_name}\n"
        
        await message.reply_text(msg)
    
    except Exception as e:
        return await message.reply_text(f"خطا: {str(e)}")

@app.on_message(filters.text & ~filters.private & ~BANNED_USERS)
async def respond_to_saved_chats(_, message):
    text = message.text.lower().strip()
    chat_id = message.chat.id
    saved_chats = await get_saved_chats(chat_id)

    for chat_name in saved_chats:
        if chat_name.lower() in text:
            chat_data = await get_saved_chats(chat_id, chat_name)
            _type = chat_data["type"]
            data = chat_data["data"]
            file_id = chat_data.get("file_id")
            
            if _type == "text":
                await message.reply_text(data)
            elif _type == "sticker":
                await message.reply_sticker(sticker=file_id)
            elif _type == "animation":
                await message.reply_animation(animation=file_id, caption=data)
            elif _type == "photo":
                await message.reply_photo(photo=file_id, caption=data)
            elif _type == "video":
                await message.reply_video(video=file_id, caption=data)
            elif _type == "audio":
                await message.reply_audio(audio=file_id, caption=data)
            return

