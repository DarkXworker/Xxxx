
import telebot
import re
import time
import threading

BOT_TOKEN = 'YOUR_BOT_TOKEN'  # 🔁 Replace this with your actual token
bot = telebot.TeleBot(BOT_TOKEN)

DELETE_DELAY = 60  # Seconds for deleting GIFs/stickers

# 🔥 Delete GIFs & Stickers after delay
@bot.message_handler(content_types=['animation', 'sticker'])
def delete_gif_sticker(message):
    def delayed_delete():
        time.sleep(DELETE_DELAY)
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print("Error deleting media:", e)
    threading.Thread(target=delayed_delete).start()

# 🌐 Delete links and warn user
@bot.message_handler(func=lambda message: bool(re.search(r'https?://|t\.me|www\.', message.text or '')))
def delete_links(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            "⚠️ Links are not allowed, even for admins!",
            reply_to_message_id=message.message_id
        )
    except Exception as e:
        print("Error deleting link:", e)

# ✅ Optional start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 I'm alive and cleaning GIFs & Links!")

bot.infinity_polling()
