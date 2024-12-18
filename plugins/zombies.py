from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# لیست کانال‌های اجباری و وضعیت جوین
forced_channels = []
join_required = True


@app.on_message(filters.text & filters.private)
async def handle_commands(client: Client, message: Message):
    text = message.text.strip().lower()

    # دستورات اضافه کردن کانال
    if text in ["اضافه کردن جوین", "add join"]:
        await message.reply("لینک یا آیدی عددی کانال را ارسال کنید:\nSend the link or numeric ID of the channel:")
        reply = await client.listen(message.chat.id)
        channel_id = reply.text.strip()

        if channel_id not in forced_channels:
            forced_channels.append(channel_id)
            await message.reply(
                f"کانال {channel_id} به لیست جوین اجباری اضافه شد.\nChannel {channel_id} has been added to the forced join list."
            )
        else:
            await message.reply(
                "این کانال قبلاً در لیست وجود دارد.\nThis channel is already in the list."
            )

    # دستورات نمایش لیست کانال‌ها
    elif text in ["نمایش لیست جوین", "show join list"]:
        if forced_channels:
            buttons = [
                [
                    InlineKeyboardButton(
                        text="عضویت در کانال / Join Channel",
                        url=f"https://t.me/{channel.replace('@', '')}",
                    )
                ]
                for channel in forced_channels
            ]
            buttons.append([InlineKeyboardButton("عضو شدم / Joined", callback_data="check_join")])
            await message.reply(
                "لیست کانال‌های جوین اجباری:\nList of forced join channels:",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            await message.reply("هیچ کانالی در لیست وجود ندارد.\nNo channels in the list.")

    # دستورات حذف کانال
    elif text in ["حذف جوین", "remove join"]:
        await message.reply("لینک یا آیدی کانالی که می‌خواهید حذف کنید را ارسال کنید:\nSend the link or ID of the channel to remove:")
        reply = await client.listen(message.chat.id)
        channel_id = reply.text.strip()

        if channel_id in forced_channels:
            forced_channels.remove(channel_id)
            await message.reply(
                f"کانال {channel_id} از لیست حذف شد.\nChannel {channel_id} has been removed from the list."
            )
        else:
            await message.reply(
                "این کانال در لیست وجود ندارد.\nThis channel is not in the list."
            )

    # دستورات روشن کردن جوین
    elif text in ["جوین روشن", "enable join"]:
        global join_required
        join_required = True
        await message.reply("جوین اجباری فعال شد.\nForced join has been enabled.")

    # دستورات خاموش کردن جوین
    elif text in ["جوین خاموش", "disable join"]:
        join_required = False
        await message.reply("جوین اجباری غیرفعال شد.\nForced join has been disabled.")


@app.on_callback_query(filters.regex("check_join"))
async def check_user_join(client: Client, callback_query):
    if join_required and forced_channels:
        user_id = callback_query.from_user.id
        not_joined = []

        for channel in forced_channels:
            try:
                await client.get_chat_member(channel, user_id)
            except:
                not_joined.append(channel)

        if not not_joined:
            await callback_query.message.reply(
                "😎 عالی! حالا می‌تونی از ربات استفاده کنی!\nAwesome! You can now use the bot!"
            )
        else:
            await callback_query.message.reply(
                "🤨 هنوز عضو همه کانال‌ها نشدی!\nYou haven't joined all the channels yet!"
            )


@app.on_message(filters.private, group=-1)
async def enforce_join(client: Client, message: Message):
    if join_required and forced_channels:
        not_joined = []

        for channel in forced_channels:
            try:
                await client.get_chat_member(channel, message.from_user.id)
            except:
                not_joined.append(channel)

        if not_joined:
            buttons = [
                [
                    InlineKeyboardButton(
                        text="عضویت در کانال / Join Channel",
                        url=f"https://t.me/{channel.replace('@', '')}",
                    )
                ]
                for channel in not_joined
            ]
            buttons.append([InlineKeyboardButton("عضو شدم / Joined", callback_data="check_join")])
            await message.reply(
                "برای استفاده از ربات، ابتدا در کانال‌های زیر عضو شوید:\nTo use the bot, join the following channels first:",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
