import os
import uuid
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from models import init_db, User, LinkToken, LinkClick

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL", "sqlite:////app/data/family_bot.db")

TARGETS = {
    "register": "https://livegoodtour.com/Aymanbenz",
    "company_video": "https://youtu.be/BmkpPgppwI4?si=7zu-jR_3ySE5wYI2",
    "earnings_video": "https://youtu.be/zcCHub9Schg?si=V2-TRzxhrKnSaLSk"
}

Session = init_db(DB_URL)

def ensure_user(session, tg_user):
    user = session.query(User).filter_by(tg_id=tg_user.id).first()
    if not user:
        user = User(
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name
        )
        session.add(user)
        session.commit()
    return user

def make_token(session, tg_id, link_key):
    token = str(uuid.uuid4())
    lt = LinkToken(token=token, tg_id=tg_id, link_key=link_key)
    session.add(lt)
    session.commit()
    return token

def start(update: Update, context: CallbackContext):
    session = Session()
    user = ensure_user(session, update.effective_user)
    t_register = make_token(session, user.tg_id, "register")
    t_company = make_token(session, user.tg_id, "company_video")
    t_earn = make_token(session, user.tg_id, "earnings_video")

    keyboard = [
        [InlineKeyboardButton("سجّل بياناتك", callback_data=f"open:{t_register}")],
        [InlineKeyboardButton("تعرّف على الشركة", callback_data=f"open:{t_company}")],
        [InlineKeyboardButton("8 مصادر لجني الأرباح", callback_data=f"open:{t_earn}")]
    ]

    text = (
        "أهلاً بك في بداية الحرية المالية!\n\n"
        "سجل بياناتك مجاناً الآن لحجز موقعك:\n"
        "https://livegoodtour.com/Aymanbenz\n\n"
        "بعد التسجيل تعرّف على الشركة:\n"
        "https://youtu.be/BmkpPgppwI4?si=7zu-jR_3ySE5wYI2\n\n"
        "والآن يمكنك معرفة 8 مصادر لجني أرباحك:\n"
        "https://youtu.be/zcCHub9Schg?si=V2-TRzxhrKnSaLSk\n\n"
        "اضغط أحد الأزرار أدناه ليتم تسجيل زيارتك:"
    )

    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    session.close()

def callback_query_handler(update: Update, context: CallbackContext):
    session = Session()
    query = update.callback_query
    data = query.data or ""

    if not data.startswith("open:"):
        query.answer()
        session.close()
        return

    token = data.split(":", 1)[1]
    lt = session.query(LinkToken).filter_by(token=token).first()

    if not lt:
        query.answer("الرابط منتهي أو غير صالح.")
        session.close()
        return

    click = LinkClick(token=token, tg_id=query.from_user.id, link_key=lt.link_key)
    session.add(click)
    session.commit()

    query.answer("تم تسجيل زيارتك — جاري إرسال الرابط...")
    target = TARGETS.get(lt.link_key)
    if target:
        query.message.reply_text(f"افتح الرابط: {target}")
    else:
        query.message.reply_text("الرابط غير متوفر حالياً.")
    session.close()

def stats(update: Update, context: CallbackContext):
    session = Session()
    total_users = session.query(User).count()
    clicks = session.query(LinkClick.link_key).all()
    from collections import Counter
    c = Counter([k for (k,) in clicks])

    lines = [f"المستخدمون المسجلون: {total_users}"]
    for key in TARGETS.keys():
        lines.append(f"{key}: {c.get(key, 0)} نقرة")

    update.message.reply_text("\n".join(lines))
    session.close()

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN غير موجود. أضفه في ملف .env")

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CallbackQueryHandler(callback_query_handler))

    print("Bot started successfully")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
