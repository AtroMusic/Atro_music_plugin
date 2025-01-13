from pyrogram import filters
from pyrogram.enums import ChatType
from strings import get_string
from YukkiMusic import app
from YukkiMusic.utils import Yukkibin
from YukkiMusic.utils.database import get_assistant, get_lang

# دستور برای نمایش اطلاعات تماس (نمایش وضعیت تماس)
@app.on_message(filters.text & filters.admin)
async def vc_members(client, message):
    if message.text == "اطلاعات تماس":
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except BaseException:
            _ = get_string("en")
        
        msg = await message.reply_text(_["V_C_1"])
        userbot = await get_assistant(message.chat.id)
        TEXT = ""
        mute_count = 0
        video_count = 0
        hand_raised_count = 0
        speaking_count = 0

        try:
            async for m in userbot.get_call_members(message.chat.id):
                chat_id = m.chat.id
                username = m.chat.username
                is_hand_raised = m.is_hand_raised
                is_video_enabled = m.is_video_enabled
                is_left = m.is_left
                is_screen_sharing_enabled = m.is_screen_sharing_enabled
                is_muted = bool(m.is_muted and not m.can_self_unmute)
                is_speaking = not m.is_muted

                # Counting based on conditions
                if is_muted:
                    mute_count += 1
                if is_video_enabled:
                    video_count += 1
                if is_hand_raised:
                    hand_raised_count += 1
                if is_speaking:
                    speaking_count += 1

                if m.chat.type != ChatType.PRIVATE:
                    title = m.chat.title
                else:
                    try:
                        title = (await client.get_users(chat_id)).mention
                    except BaseException:
                        title = m.chat.first_name

                TEXT += _["V_C_2"].format(
                    title,
                    chat_id,
                    username,
                    is_video_enabled,
                    is_screen_sharing_enabled,
                    is_hand_raised,
                    is_muted,
                    is_speaking,
                    is_left,
                )
                TEXT += "\n\n"

            TEXT += "\n\n" + _["V_C_STATS"].format(mute_count, video_count, hand_raised_count, speaking_count)
            await msg.edit(TEXT or _["V_C_3"])
        except ValueError as e:
            await msg.edit(_["V_C_5"])

# دستور تغییر عنوان گروه
@app.on_message(filters.text & filters.admin)
async def change_vc_title(client, message):
    if message.text.startswith("تغییر عنوان گفتگو "):
        new_title = message.text[len("تغییر عنوان گفتگو "):].strip()
        
        if new_title:
            try:
                userbot = await get_assistant(message.chat.id)
                await userbot.set_chat_title(message.chat.id, new_title)
                await message.reply_text(f"عنوان گفتگو به '{new_title}' تغییر یافت.")
                
                # اطلاع رسانی به اعضای گروه در صورت تغییر عنوان
                await message.reply_text(f"توجه: عنوان گروه به '{new_title}' تغییر یافت.")
            except Exception as e:
                await message.reply_text(f"خطا در تغییر عنوان: {str(e)}")
        else:
            await message.reply_text("لطفاً عنوان جدید را وارد کنید. استفاده: تغییر عنوان گفتگو <عنوان جدید>")

# دستور کمک (help) برای راهنمایی دستورات
@app.on_message(filters.text & filters.command("help"))
async def help_message(client, message):
    help_text = """
    دستورات ربات:

    1. اطلاعات تماس: نمایش اطلاعات تماس و اعضای گروه.
    2. تغییر عنوان گفتگو <عنوان جدید>: تغییر عنوان گروه یا تماس به عنوان جدید.
    3. پخش موسیقی: وضعیت پخش موسیقی را نمایش می‌دهد.
    """
    await message.reply_text(help_text)

# دستور نمایش وضعیت پخش موسیقی
@app.on_message(filters.text & filters.admin)
async def music_status(client, message):
    if message.text == "وضعیت موسیقی":
        try:
            # فرض بر این است که ربات موسیقی پخش می‌کند و اطلاعات آن در یک متغیر یا دیتابیس ذخیره می‌شود
            status = "موسیقی در حال پخش است."  # این وضعیت را می‌توانید براساس وضعیت واقعی ربات تنظیم کنید.
            await message.reply_text(status)
        except Exception as e:
            await message.reply_text(f"خطا در دریافت وضعیت موسیقی: {str(e)}")
