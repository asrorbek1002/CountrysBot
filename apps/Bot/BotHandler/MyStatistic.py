from telegram.ext import ContextTypes
from ..models.TelegramBot import TelegramUser   
from asgiref.sync import sync_to_async
from telegram import Update
import pytz
from datetime import datetime

async def my_statistic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await sync_to_async(TelegramUser.objects.get)(user_id=update.effective_user.id)
    
    # Aniqlikni hisoblash (0 bo'lishini oldini olish)
    accuracy = 0
    if user.total_questions_answered > 0:
        accuracy = round((user.correct_answers / user.total_questions_answered) * 100, 1)
    
    # Toshkent vaqt zonasini olish
    tashkent_tz = pytz.timezone('Asia/Tashkent')
    
    # Oxirgi o'yin vaqtini Toshkent vaqtiga o'tkazish
    last_quiz_time = user.last_quiz_date.astimezone(tashkent_tz) if user.last_quiz_date else None
    
    # Foydalanuvchi qo'shilgan vaqtini Toshkent vaqtiga o'tkazish
    joined_date = user.date_joined.astimezone(tashkent_tz)
    
    # Foydalanuvchi qancha vaqtdan beri botda ekanligini hisoblash
    now = datetime.now(tashkent_tz)
    days_in_bot = (now - joined_date).days
    
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"📊 <b>Statistika</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {user.first_name}\n"
        f"📅 <b>Botda:</b> {days_in_bot} kun\n"
        f"━━━━━━━━━━━━━━\n"
        f"📝 <b>Jami savollar:</b> {user.total_questions_answered} ta\n"
        f"✅ <b>To'g'ri javoblar:</b> {user.correct_answers} ta\n"
        f"❌ <b>Xato javoblar:</b> {user.wrong_answers} ta\n"
        f"🎯 <b>Aniqlik darajasi:</b> {accuracy}%\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕐 <b>Oxirgi o'yin:</b> {last_quiz_time.strftime('%d.%m.%Y %H:%M') if last_quiz_time else 'Hali o\'ynamagan'}\n"
        f"📌 <b>Botga qo'shilgan:</b> {joined_date.strftime('%d.%m.%Y %H:%M')}",
        parse_mode="HTML"
    )
