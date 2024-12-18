MohammaD, [12/17/2024 10:34 PM]
import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# لیست بیوگرافی‌ها
BIOGRAPHIES = [
    "زندگی کوتاه است، اما خاطرات آن طولانی.",
    "تنهایی را دوست دارم، چون کسی نیست که دلم را بشکند.",
    "غم‌هایم را می‌نویسم، شاید کسی بخواند و بفهمد.",
    "تو فقط خاطره‌ای هستی که هنوز زنده است.",
    "عشق، گاهی شروعی است برای پایان.",
    "هر روزی که بی تو می‌گذرد، یک قرن است.",
    "کاش دلی بود که به اندازه من تنگ تو می‌شد.",
    "زندگی‌ام را با خنده‌های مصنوعی پر کرده‌ام.",
    "گاهی دلتنگی برای کسی که نیست، عجیب زیباست.",
    "تو همان کسی هستی که نبودنت هم درد می‌آورد.",
    "اگر عشق جنون است، من دیوانه‌ترینم.",
    "تنهایی یعنی هزار نفر دور و برت باشند و تو باز دلتنگ باشی.",
    "هر زخم داستانی دارد، اما همه داستان‌ها شنیدنی نیستند.",
    "تو برای من تمام دنیا بودی، اما من برای تو فقط یک لحظه.",
    "زندگی چیزی نیست جز بازی احساسات و خاطرات.",
    "دلم برای روزهایی که هنوز ندیدمت تنگ است.",
    "غم و شادی هر دو می‌گذرند، اما زخم‌های عشق ماندنی‌اند.",
    "زندگی‌ام را در سکوت سپری می‌کنم، چون کسی صدایم را نمی‌شنود.",
    "تو رفتی و من هنوز منتظر بازگشتت هستم.",
    "خاطراتت مثل یک فیلم تکراری، هر شب در ذهنم پخش می‌شود.",
    "عشق یعنی تو، حتی اگر من نباشم.",
    "کاش می‌توانستم فقط یک بار دیگر نگاهت کنم.",
    "هرگز به کسی که دوستش داری نگو خداحافظ، شاید آخرین خداحافظی باشد.",
    "من همان عاشقی هستم که هیچ‌کس عشقش را باور نکرد.",
    "غمگینم، اما هنوز به امید دیدنت زنده‌ام.",
    "هر دل شکسته‌ای داستانی دارد که هیچ‌کس آن را نمی‌داند.",
    "گاهی درد، تنها دوای زخم‌های قدیمی است.",
    "تو رفته‌ای، اما خاطراتت هنوز با من زندگی می‌کنند.",
    "عشق واقعی هرگز نمی‌میرد، حتی اگر فراموش شود.",
    "وقتی رفتی، بخشی از من را با خودت بردی.",
    "اشک‌هایم از لبخندم صادقانه‌تر هستند.",
    "هر چقدر تلاش کنم، نمی‌توانم از یاد تو بگذرم.",
    "گاهی وقت‌ها فکر می‌کنم، آیا تو هم به من فکر می‌کنی؟",
    "تنهایی جایی است که در آن خاطرات بیشتر از افراد واقعی هستند.",
    "بی تو دنیا یک کتاب خالی است.",
    "به یاد تو می‌خندم، اما دلم می‌گرید.",
    "خاطرات ما مثل زخم‌هایی هستند که همیشه تازه می‌مانند.",
    "تو دلیل اشک‌ها و لبخندهای منی.",
    "کاش می‌توانستم تمام خاطراتت را پاک کنم، اما نمی‌توانم.",
    "تو دلیل تمام شعرهای غمگین من هستی.",
    "هر شب با خیالت می‌خوابم و هر صبح بدون تو بیدار می‌شوم.",
    "زندگی بدون تو مثل آسمان بدون ستاره است.",
    "گاهی وقت‌ها فقط نگاه به عکس‌های قدیمی کافی است که قلبت هزار بار بشکند.",
    "قلبم هنوز در همان روزی گیر کرده که تو رفتی.",
    "زمان همه چیز را درمان می‌کند، اما تو را نه.",
    "زندگی بدون تو مثل آهنگی است که متن آن گم شده.",
    "تو مرا به جایی رساندی که نمی‌توانم برگردم.",
    "هرگز فکر نمی‌کردم، عشق این‌قدر درد داشته باشد.",
    "گاهی وقت‌ها دوست دارم فقط برای یک لحظه دوباره ببینمت.",
    "خاطرات تو مثل سایه، همیشه همراه من هستند.",
    "با رفتنت، آسمان دنیای من تاریک شد.",
    "هرگز به کسی اعتماد نکن که توانایی شکستن قلبت را دارد.",
    "دردناک‌ترین خداحافظی، آن است که هرگز گفته نشد.",
    "تو دنیای من بودی، اما حالا فقط یک خاطره‌ای.",
    "تنهایی یعنی وقتی که همه‌چیز را داری، ولی چیزی نداری.",
    "خاطرات خوب از قلب دردناک می‌آیند.",
    "گاهی اوقات، تنها چیزی که باقی می‌ماند، اشک است.",
    "من همیشه درگیر توام، حتی وقتی که نمی‌بینمت.",
    "یاد تو، یکی از بهترین اتفاقات زندگی‌ام بود.",
    "هر کسی یک روز خواهد رفت، ولی بعضی‌ها همیشه می‌مانند.",
    "هیچ‌چیزی سخت‌تر از دیدن یک غمگین‌ترین روز است.",
    "دل من همواره در انتظار تو خواهد بود.",
    "دلم برای روزهایی که با تو بودم تنگ است.",
    "غم بزرگ‌تر از آن است که در کلمات جا شود.",
    "با رفتن تو، دنیایم خاموش شد.",
    "اگر قلبم را شکستی، یادم باشد که خودت را فراموش نکنی.",
    "زندگی بدون تو مثل شب بدون ماه است.",
    "گاهی به آن روزهایی فکر می‌کنم که تو هنوز در کنارم بودی.",
    "دلتنگی تنها چیزی است که از تو باقی مانده.",

MohammaD, [12/17/2024 10:34 PM]
"گاهی آدم‌ها مثل سایه‌ها می‌آیند و می‌روند.",
    "دوست داشتن گاهی مانند آتش می‌سوزاند.",
    "تو رفته‌ای، اما دلتنگی‌ها باقی‌مانده‌اند.",
    "شکستن قلب هیچ‌وقت آسان نیست.",
    "همه چیز می‌گذرد، جز تو.",
    "دل شکسته، به دردهای بی‌پایان می‌ماند.",
    "هر چه زمان می‌گذرد، درد غم بیشتر می‌شود.",
    "برای فراموش کردن، باید هر لحظه با یاد تو زندگی کنم.",
    "نمی‌توانم به یاد تو پایان دهم.",
    "وقتی برای اولین‌بار عاشق می‌شوی، هیچ چیزی همانطور نمی‌ماند.",
    "تویی که وقتی نیستی، دلم را پر از آرزوهای دست‌نیافتنی می‌کنی.",
    "هر روز که می‌گذرد، بیشتر دلتنگت می‌شوم.",
    "عشق یعنی حتی در زمان فاصله‌ها، همیشه با کسی در دل باشی.",
    "تو رفتی، ولی بخش‌هایی از دلم هنوز با توست.",
    "در انتظار کسی که هنوز نرسیده است.",
    "من به خاطر تو خودم را از دست دادم، ولی هنوز در جستجوی خودم هستم.",
    "بعضی‌ها یادشان می‌رود، بعضی‌ها برای همیشه در قلبت باقی می‌مانند.",
    "دلم برای لحظاتی که با تو گذراندم تنگ است.",
    "با رفتنت، آسمان زندگی‌ام ابر شد.",
]

@app.on_message(filters.text & ~filters.edited)  # پوشش چت‌های خصوصی و گروهی
async def get_bio(_, message):
    if message.text.strip() in ["بیو", "بیوگرافی"]:  # بررسی دستورات فارسی
        random_bio = random.choice(BIOGRAPHIES)
        refresh_button = InlineKeyboardButton("تازه‌سازی", callback_data="refresh_bio")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[refresh_button]])
        await message.reply_text(
            random_bio, reply_markup=keyboard, parse_mode=ParseMode.HTML
        )


@app.on_callback_query(filters.regex(r"refresh_bio"))
async def refresh_bio(_, query):
    await query.answer()
    new_bio = random.choice(BIOGRAPHIES)
    await query.message.edit_text(
        new_bio,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("تازه‌سازی", callback_data="refresh_bio")]]
        ),
        parse_mode=ParseMode.HTML,
    )
