import random
from pyrogram import Client, filters
from YukkiMusic import app
import time

# سوالات و چالش‌ها (بیشتر و متنوع‌تر)
truth_questions = [
    "چه چیزی را هیچ‌گاه کسی از شما نمی‌داند؟",
    "اگر فقط یک روز زندگی می‌کردید، چه کار می‌کردید؟",
    "چه چیزی را بیشتر از هر چیز دیگری پنهان می‌کنید؟",
    "بزرگ‌ترین ترس شما چیست؟",
    "آیا تاکنون به کسی دروغ گفته‌اید؟",
    "چه چیزی از شما بسیار جالب است که دیگران نمی‌دانند؟"
]

dare_challenges = [
    "۱۰ بار پشتک بزن.",
    "۱۰ دقیقه بخند بدون اینکه حرف بزنی.",
    "با صدای بلند در اتاق بخوان.",
    "یک تماس ویدیویی با دوستان خود بگیرید و آنها را به خنده بیندازید.",
    "هر چیزی که نزدیکت هست رو به مدت یک دقیقه دستکاری کن."
]

# سوالات و چالش‌های سخت
hard_truth_questions = [
    "بزرگ‌ترین اشتباهی که در زندگی کرده‌ای چیست؟",
    "آیا تاکنون به بهترین دوستت خیانت کرده‌ای؟",
    "چه رازی را از پدر و مادرت پنهان کرده‌ای؟",
    "اگر تنها یک ساعت برای زندگی داشتید، چه می‌کردید؟"
]

hard_dare_challenges = [
    "۲۰ دقیقه بدون هیچ حرفی در یک اتاق تنها بمان.",
    "تا زمانی که کسی نمی‌بیند، ۵ بار جلیقه ات را به عقب بزن.",
    "تمام دست‌هایت را بزن به صورت خود و ۵ دقیقه صبر کن."
]

# سوالات و چالش‌های +18
truth_questions_18 = [
    "چه چیزی از شماست که هیچ‌کس از آن مطلع نیست؟",
    "آیا تاکنون در موقعیت‌های جنسی خطرناک بوده‌ای؟",
    "آیا تا به حال با کسی رابطه عاشقانه برقرار کرده‌ای که حتی فکرش را هم نمی‌کردی؟"
]

dare_challenges_18 = [
    "باید ۵ دقیقه در یک اتاق تاریک تنها بمانی.",
    "مقداری از یک غذای غیرمعمول یا ناخوشایند را بخور.",
    "لباس خود را تغییر ده و به همه نشان بده.",
    "۱۵ دقیقه به کسی زنگ بزن و داستانی بسیار خنده‌دار تعریف کن."
]

# سوالات و چالش‌های ویژه (کلید شیشه‌ای)
special_truth_questions = [
    "آیا تاکنون به کسی خیانت کرده‌ای؟",
    "اگر فرصت داشتی به گذشته بازگردی، چه چیزی را تغییر می‌دادی؟"
]

special_dare_challenges = [
    "یک نفر را در گروه نام ببر و بگو چه چیزی را بیشتر از همه دوست داری که او انجام دهد!",
    "شما باید به کسی در گروه یک راز خود را بگویید که هیچ‌گاه نمی‌گفته‌اید."
]

# ذخیره‌سازی امتیاز کاربران
user_scores = {}

# انتخاب نوع سوال
@app.on_message(filters.command("حقیقت"))
async def get_truth(client, message):
    try:
        difficulty = "easy"
        if len(message.text.split()) > 1 and message.text.split()[1] == "سخت":
            difficulty = "hard"
        if len(message.text.split()) > 1 and message.text.split()[1] == "ویژه":
            difficulty = "special"
        if len(message.text.split()) > 1 and message.text.split()[1] == "+18":
            difficulty = "18"

        if difficulty == "hard":
            question = random.choice(hard_truth_questions)
        elif difficulty == "special":
            question = random.choice(special_truth_questions)
        elif difficulty == "18":
            question = random.choice(truth_questions_18)
        else:
            question = random.choice(truth_questions)

        # اضافه کردن امتیاز
        user_scores[message.from_user.id] = user_scores.get(message.from_user.id, 0) + 1

        await message.reply_text(f"سوال حقیقت: {question}")
    except Exception as e:
        await message.reply_text("خطا در دریافت سوال حقیقت. لطفاً بعداً دوباره امتحان کنید.")

@app.on_message(filters.command("جرعت"))
async def get_dare(client, message):
    try:
        difficulty = "easy"
        if len(message.text.split()) > 1 and message.text.split()[1] == "سخت":
            difficulty = "hard"
        if len(message.text.split()) > 1 and message.text.split()[1] == "ویژه":
            difficulty = "special"
        if len(message.text.split()) > 1 and message.text.split()[1] == "+18":
            difficulty = "18"

        if difficulty == "hard":
            challenge = random.choice(hard_dare_challenges)
        elif difficulty == "special":
            challenge = random.choice(special_dare_challenges)
        elif difficulty == "18":
            challenge = random.choice(dare_challenges_18)
        else:
            challenge = random.choice(dare_challenges)

        # اضافه کردن امتیاز
        user_scores[message.from_user.id] = user_scores.get(message.from_user.id, 0) + 1

        await message.reply_text(f"چالش جرعت: {challenge}")
    except Exception as e:
        await message.reply_text("خطا در دریافت چالش جرعت. لطفاً بعداً دوباره امتحان کنید.")

# دستور /کمک
@app.on_message(filters.command("کمک"))
async def help(client, message):
    help_text = """
**دستورات بازی حقیقت و جرعت**

- `/حقیقت`: دریافت یک سوال حقیقت.
- `/جرعت`: دریافت یک چالش جرعت.
- `/حقیقت سخت`: دریافت یک سوال حقیقت سخت.
- `/جرعت سخت`: دریافت یک چالش جرعت سخت.
- `/حقیقت ویژه`: دریافت یک سوال حقیقت ویژه.
- `/جرعت ویژه`: دریافت یک چالش جرعت ویژه.
- `/حقیقت +18`: دریافت یک سوال حقیقت +18.
- `/جرعت +18`: دریافت یک چالش جرعت +18.
- `/بازی`: بازی چند نفره با سوالات و چالش‌های تصادفی.
- `/امتیاز`: مشاهده امتیاز خود.
- `/آمار`: مشاهده آمار بازی‌ها و رکوردها.

**نمونه‌ها:**
- `/حقیقت`: سوال حقیقت معمولی.
- `/جرعت`: چالش جرعت معمولی.
- `/حقیقت سخت`: سوال حقیقت سخت.
- `/جرعت سخت`: چالش جرعت سخت.
- `/حقیقت +18`: سوال حقیقت +18.
- `/جرعت +18`: چالش جرعت +18.

**نکات:**
اگر با خطا مواجه شدید، لطفاً دوباره امتحان کنید.
    """
    await message.reply_text(help_text)

# دستور /امتیاز برای نمایش امتیاز کاربران
@app.on_message(filters.command("امتیاز"))
async def show_score(client, message):
    user_id = message.from_user.id
    score = user_scores.get(user_id, 0)
    await message.reply_text(f"امتیاز شما: {score}")

# دستور برای بازی چند نفره (حقیقت و جرعت برای اعضای گروه)
@app.on_message(filters.command("بازی"))
async def play_game(client, message):
    members = await message.chat.get_members()
    players = random.sample(members, 3)  # انتخاب 3 نفر به صورت تصادفی از اعضا

    truth_player = random.choice(players)
    dare_player = random.choice(players)

    truth_question = random.choice(truth_questions)
    dare_challenge = random.choice(dare_challenges)

    await message.reply_text(f"سوال حقیقت برای {truth_player.mention}:\n{truth_question}")
    await message.reply_text(f"چالش جرعت برای {dare_player.mention}:\n{dare_challenge}")

