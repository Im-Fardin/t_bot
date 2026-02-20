import os
from flask import Flask, request
import telebot
from telebot import types
from dotenv import load_dotenv
from query import add_or_update_user, get_channel_link

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # e.g., https://your-server.com

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)
user_data = {}

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

# --- Telegram Webhook Endpoint ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# --- Health Check ---
@app.route("/")
def index():
    return "Bot is running!", 200

# --- Set Webhook Automatically ---
@app.before_first_request
def setup_webhook():
    if WEBHOOK_URL:
        webhook_full = f"{WEBHOOK_URL}/{BOT_TOKEN}"
        bot.remove_webhook()
        bot.set_webhook(url=webhook_full)
        print(f"Webhook set to {webhook_full}")
    else:
        print("WEBHOOK_URL not set in .env, skipping automatic webhook setup.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))