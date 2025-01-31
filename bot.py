import telebot
from config import TOKEN
from db import create_tables, add_message, get_recent_messages
import time

bot = telebot.TeleBot(TOKEN)

def mute_user(chat_id, user_id, duration):
    bot.restrict_chat_member(chat_id, user_id, until_date=int(time.time()) + duration, can_send_messages=False)

@bot.message_handler(content_types=['text', 'sticker', 'animation'])
def handle_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    content = message.text if message.content_type == 'text' else message.content_type
    
    create_tables(chat_id)
    add_message(chat_id, user_id, content)
    
    recent_messages = get_recent_messages(chat_id, user_id)
    
    if len(recent_messages) > 5 and all(msg[0] == content for msg in recent_messages):
        mute_user(chat_id, user_id, 60)
        user_link = f'<a href="tg://user?id={user_id}">{message.from_user.first_name}</a>'
        bot.send_message(chat_id, f"Пользователь {user_link} замучен на минуту за спам.", parse_mode='HTML')

bot.infinity_polling()