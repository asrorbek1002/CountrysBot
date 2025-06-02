from ..MandatoryChannel import AddChannel_ConvHandler, MandatoryChannelOrGroupList, start_delete_mandatory, delete_mandatory
from ..BotCommands import start
from ..BotAdmin import admin_menyu, add_admin_handler, the_first_admin, remove_admin_handler, AdminList
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from ..BotHandler import send_msg_handler, bot_stats, edit_bot_bio, InlineButton
from datetime import datetime, timedelta
from ..BotCommands.DownDB import DownlBD
import random
import os 
from dotenv import load_dotenv

load_dotenv()

# Bot Token
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")


async def schedule_next_bio_update(context):
    # Keyingi bio yangilanishi uchun 10-12 soat oralig'ida tasodifiy vaqt tanlash
    hours = random.uniform(10, 12)
    next_time = datetime.now() + timedelta(hours=hours)
    
    # Joriy bio yangilanishini bajarish
    await edit_bot_bio(None, context)
    
    # Keyingi yangilanishni rejalashtirish
    context.job_queue.run_once(schedule_next_bio_update, 
                             when=next_time)

def main():
    # Application yaratishda persistence va job_queue parametrlarini qo'shamiz
    app = Application.builder().token(TOKEN).build()

    # Commands  
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("DownDataBaza", DownlBD))
    app.add_handler(CommandHandler('admin_panel', admin_menyu))
    app.add_handler(CommandHandler('kjiaufuyerfgvu', the_first_admin))
    app.add_handler(CommandHandler('edit_bot_bio', edit_bot_bio))
    
    # Conversation handlers
    app.add_handler(send_msg_handler)
    app.add_handler(add_admin_handler)
    app.add_handler(remove_admin_handler)
    app.add_handler(AddChannel_ConvHandler)


    # Inline hanlder
    app.add_handler(CallbackQueryHandler(start, pattern=r"^Main_Menu$"))
    app.add_handler(CallbackQueryHandler(bot_stats, pattern=r"^botstats$"))
    app.add_handler(CallbackQueryHandler(start, pattern=r"^cancel$"))
    app.add_handler(CallbackQueryHandler(start_delete_mandatory, pattern=r"^Del_mandatory$"))
    app.add_handler(CallbackQueryHandler(delete_mandatory, pattern=r"^xDeleted_"))
    app.add_handler(CallbackQueryHandler(start, pattern=r"^Check_mandatory_channel$"))
    app.add_handler(CallbackQueryHandler(AdminList, pattern=r"^admin_list$"))
    app.add_handler(CallbackQueryHandler(MandatoryChannelOrGroupList, pattern=r"^mandatory_channel$"))
    app.add_handler(CallbackQueryHandler(start, pattern=r"^BackToMainMenu$"))
    app.add_handler(CallbackQueryHandler(InlineButton))

    
    # Schedule
    if app.job_queue:  # job_queue mavjudligini tekshiramiz
        # Birinchi yangilanishni boshlash
        app.job_queue.run_once(schedule_next_bio_update, 
                          when=datetime.now())
    
    # Bot start
    print("The bot is running!!!")
    app.run_polling()
