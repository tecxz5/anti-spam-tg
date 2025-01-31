import telebot
from config import TOKEN
from db import create_tables, update_user, get_punishments, increment_punishments, add_message, get_recent_messages
import time

bot = telebot.TeleBot(TOKEN)

# Функция для мутирования пользователя
def mute_user(chat_id, user_id, duration):
    bot.restrict_chat_member(chat_id, user_id, until_date=int(time.time()) + duration, can_send_messages=False)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text', 'sticker', 'animation'])
def handle_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    content = message.text if message.content_type == 'text' else message.content_type
    
    create_tables(chat_id)
    update_user(chat_id, user_id)
    add_message(chat_id, user_id, content)
    
    recent_messages = get_recent_messages(chat_id, user_id)
    
    if len(recent_messages) > 5 and all(msg[0] == content for msg in recent_messages):
        increment_punishments(chat_id, user_id)
        punishments = get_punishments(chat_id, user_id)
        mute_durations = [60, 300, 600]
        
        if punishments > 3:
            duration = mute_durations[2]
        elif punishments == 3:
            duration = mute_durations[1]
        else:
            duration = mute_durations[0]
        
        mute_user(chat_id, user_id, duration)
        bot.send_message(chat_id, f"Пользователь {message.from_user.first_name} замучен на {duration // 60} минут(ы) за спам.")

@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Привет! Я антиспам бот. Я буду следить за спамом в группах.")
    else:
        return

bot.infinity_polling()