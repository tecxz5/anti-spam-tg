import telebot
from config import TOKEN
import time
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='log.txt', encoding='utf-8')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)
user_messages = defaultdict(lambda: deque(maxlen=3))

def mute_user(chat_id, user_id, duration):
    bot.restrict_chat_member(chat_id, user_id, until_date=int(time.time()) + duration, can_send_messages=False)
    logger.info(f"User {user_id} has been muted in chat {chat_id} for {duration} seconds.")

@bot.message_handler(content_types=['text', 'sticker', 'animation', 'dice'])
def handle_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()
    
    content = message.text if message.content_type == 'text' else message.content_type
    logger.info(f"Received message from user {user_id} in chat {chat_id}: {content}")
    
    user_messages[(chat_id, user_id)].append(current_time)
    
    recent_messages = user_messages[(chat_id, user_id)]
    if len(recent_messages) == 3 and (current_time - recent_messages[0]) <= 8:
        mute_user(chat_id, user_id, 60)
        user_link = f'<a href="tg://user?id={user_id}">{message.from_user.first_name}</a>'
        bot.send_message(chat_id, f"Пользователь {user_link} замучен на минуту за спам.", parse_mode='HTML')
        user_messages[(chat_id, user_id)].clear()
        logger.info(f"User {user_id} has been muted for spamming in chat {chat_id}.")

bot.infinity_polling()