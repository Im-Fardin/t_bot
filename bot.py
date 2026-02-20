import telebot
from telebot import types
from database import add_or_update_user, get_channel_link

TOKEN = "8586626106:AAHkG6mI7EXrPiwXK8pUCL01jUZxCJO_S1I"  
bot = telebot.TeleBot(TOKEN)

user_data = {}

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

    # Save user in database
    add_or_update_user(chat_id, name, phone)

    # Get channel link
    channel_link = get_channel_link()

    bot.send_message(chat_id, f"✅ {name} عزیز، ممنون! لینک کانال شما:\n{channel_link}")
    user_data.pop(chat_id, None)

bot.infinity_polling()