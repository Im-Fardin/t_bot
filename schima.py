# schema.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
DEFAULT_CHANNEL = "https://t.me/hurshopco"

def create_tables():
    """Ensure the database tables exist and insert default channel if needed."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id BIGINT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            joined_at TIMESTAMP
        )
        """)

        # Channels table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id SERIAL PRIMARY KEY,
            channel_link TEXT,
            description TEXT
        )
        """)

        # Insert default channel if not exists
        cursor.execute("SELECT COUNT(*) FROM channels")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO channels (channel_link, description) VALUES (%s, %s)",
                (DEFAULT_CHANNEL, "کانال اصلی")
            )

        cursor.close()
        conn.close()
        print("✅ Database tables ensured.")
    except Exception as e:
        print(f"ERROR creating tables: {e}")