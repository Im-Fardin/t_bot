import os
from fastapi import FastAPI, Request
import telebot
from telebot import types
from query import add_or_update_user, get_channel_link
from dotenv import load_dotenv
import uvicorn

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8000))
WEBHOOK_PATH = f"/{TOKEN}/"  # secret path

bot = telebot.TeleBot(TOKEN, threaded=False)
user_data = {}
app = FastAPI()

# --- Bot Handlers ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "سلام 👋\nلطفا نام خود را وارد کنید:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id] = {"name": message.text}
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn = types.KeyboardButton("ارسال شماره تماس", request_contact=True)
    markup.add(btn)
    bot.send_message(message.chat.id, "لطفا شماره تماس خود را ارسال کنید:", reply_markup=markup)
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    chat_id = message.chat.id
    name = user_data[chat_id]["name"]
    phone = message.contact.phone_number if message.contact else message.text

    add_or_update_user(chat_id, name, phone)
    channel_link = get_channel_link()
    bot.send_message(chat_id, f"✅ {name} عزیز، ممنون! لینک کانال شما:\n{channel_link}")
    user_data.pop(chat_id, None)

# --- FastAPI Webhook Route ---
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    json_data = await request.json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return {"status": "ok"}

# --- Startup: set webhook ---
@app.on_event("startup")
async def on_startup():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)
    print(f"Webhook set to {WEBHOOK_URL + WEBHOOK_PATH}")

# --- Run Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)