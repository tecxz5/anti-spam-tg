import sqlite3
import time

def create_tables(chat_id):
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f'''CREATE TABLE IF NOT EXISTS group_{chat_id}_users (
                    user_id INTEGER PRIMARY KEY,
                    punishments INTEGER DEFAULT 0)''')
    cur.execute(f'''CREATE TABLE IF NOT EXISTS group_{chat_id}_messages (
                    user_id INTEGER,
                    message TEXT,
                    timestamp INTEGER)''')
    conn.commit()
    conn.close()

def update_user(chat_id, user_id):
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f"SELECT punishments FROM group_{chat_id}_users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row is None:
        cur.execute(f"INSERT INTO group_{chat_id}_users (user_id, punishments) VALUES (?, ?)", (user_id, 0))
    conn.commit()
    conn.close()

def get_punishments(chat_id, user_id):
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f"SELECT punishments FROM group_{chat_id}_users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def increment_punishments(chat_id, user_id):
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE group_{chat_id}_users SET punishments = punishments + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def add_message(chat_id, user_id, message):
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO group_{chat_id}_messages (user_id, message, timestamp) VALUES (?, ?, ?)",
                (user_id, message, int(time.time())))
    conn.commit()
    conn.close()

def get_recent_messages(chat_id, user_id, time_frame=3):
    conn = sqlite3.connect('groups.db')
    cur = conn.cursor()
    cur.execute(f"SELECT message, timestamp FROM group_{chat_id}_messages WHERE user_id = ? AND timestamp > ?",
                (user_id, int(time.time()) - time_frame))
    rows = cur.fetchall()
    conn.close()
    return rows