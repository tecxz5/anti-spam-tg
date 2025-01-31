import sqlite3
import time

def create_tables(chat_id):
    table_name_messages = f"group_{abs(chat_id)}_messages"
    
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_messages} (
                    user_id INTEGER,
                    message TEXT,
                    timestamp INTEGER)''')
    conn.commit()
    conn.close()

def add_message(chat_id, user_id, message):
    table_name_messages = f"group_{abs(chat_id)}_messages"
    
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name_messages} (user_id, message, timestamp) VALUES (?, ?, ?)",
                (user_id, message, int(time.time())))
    conn.commit()
    conn.close()

def get_recent_messages(chat_id, user_id, time_frame=3):
    table_name_messages = f"group_{abs(chat_id)}_messages"
    
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f"SELECT message, timestamp FROM {table_name_messages} WHERE user_id = ? AND timestamp > ?",
                (user_id, int(time.time()) - time_frame))
    rows = cur.fetchall()
    conn.close()
    return rows