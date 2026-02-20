import sqlite3
from datetime import datetime

DB_FILE = "bot.db"
DEFAULT_CHANNEL = "https://t.me/hurshopco"

# --- Connect to database ---
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# --- Create tables ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    chat_id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    joined_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_link TEXT,
    description TEXT
)
""")
conn.commit()

# --- Insert default channel if none exists ---
cursor.execute("SELECT COUNT(*) FROM channels")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO channels (channel_link, description) VALUES (?, ?)",
        (DEFAULT_CHANNEL, "کانال اصلی")
    )
    conn.commit()

# --- Helper functions ---
def add_or_update_user(chat_id, name, phone):
    joined_at = datetime.now().isoformat()
    cursor.execute("""
        INSERT OR REPLACE INTO users (chat_id, name, phone, joined_at)
        VALUES (?, ?, ?, ?)
    """, (chat_id, name, phone, joined_at))
    conn.commit()

def get_channel_link():
    cursor.execute("SELECT channel_link FROM channels LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else None