import os
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Бот запущен. Готов работать.")

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

if __name__ == "__main__":
    bot.infinity_polling()
