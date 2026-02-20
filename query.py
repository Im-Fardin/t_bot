import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def add_or_update_user(chat_id, name, phone):
    joined_at = datetime.now()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (chat_id, name, phone, joined_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (chat_id)
        DO UPDATE SET name = EXCLUDED.name,
                      phone = EXCLUDED.phone,
                      joined_at = EXCLUDED.joined_at
    """, (chat_id, name, phone, joined_at))
    conn.commit()
    cursor.close()
    conn.close()

def get_channel_link():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_link FROM channels LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None