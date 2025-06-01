from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests
from datetime import datetime
from asgiref.sync import sync_to_async
from ..decorators import typing_action


def get_random_fun_fact():
    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def today_date():
    return datetime.now().strftime("%Y-%m-%d")



@typing_action
async def random_fun_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Avval reaksiya qo'shamiz

    fact = get_random_fun_fact()
    reply_markup = [
        [InlineKeyboardButton(text="🧩 Other fact", callback_data='random_facts')],
        [InlineKeyboardButton(text="🏠 Back to main menu", callback_data='BackToMainMenu')]
    ]

    
    await update.callback_query.edit_message_text(
        f"<b>� Random fun fact</b>\n\n{fact.text}", 
        parse_mode="HTML", 
        reply_markup=InlineKeyboardMarkup(reply_markup)
    )