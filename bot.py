import telebot
from config import TOKEN
import time
from collections import defaultdict, deque
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)
user_messages = defaultdict(lambda: deque(maxlen=6))

def mute_user(chat_id, user_id, duration):
    bot.restrict_chat_member(chat_id, user_id, until_date=int(time.time()) + duration, can_send_messages=False)
    logger.info(f"User {user_id} has been muted in chat {chat_id} for {duration} seconds.")

@bot.message_handler(content_types=['text', 'sticker', 'animation', 'dice'])
def handle_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()
    
    # Логируем сообщение
    logger.info(f"Received message from user {user_id} in chat {chat_id}: {message.text or message.content_type}")
    
    # Добавляем сообщение в очередь
    user_messages[(chat_id, user_id)].append(current_time)
    
    # Проверяем на спам
    recent_messages = user_messages[(chat_id, user_id)]
    if len(recent_messages) == 6 and (current_time - recent_messages[0]) <= 3:
        mute_user(chat_id, user_id, 60)
        user_link = f'<a href="tg://user?id={user_id}">{message.from_user.first_name}</a>'
        bot.send_message(chat_id, f"Пользователь {user_link} замучен на минуту за спам.", parse_mode='HTML')
        user_messages[(chat_id, user_id)].clear()  # Очищаем очередь сообщений пользователя
        logger.info(f"User {user_id} has been muted for spamming in chat {chat_id}.")

bot.infinity_polling()