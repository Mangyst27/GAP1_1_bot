import os
import telebot
from rembg import remove
from PIL import Image
import io

# Токен будет браться из переменных окружения (настроим их на Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для создания карточек Wildberries. Отправь мне фото товара.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "⏳ Обрабатываю фото. Это может занять 10-15 секунд...")
    
    try:
        # 1. Скачиваем фото от пользователя
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # 2. Удаляем фон (магия нейросети)
        input_image = Image.open(io.BytesIO(downloaded_file))
        output_image = remove(input_image)
        
        # 3. Создаем чистый белый фон 900x1200 (стандарт WB)
        background = Image.new('RGBA', (900, 1200), (255, 255, 255, 255))
        
        # 4. Вписываем товар в размеры
        output_image.thumbnail((800, 800))
        
        # 5. Центрируем товар на фоне
        x = (background.width - output_image.width) // 2
        y = (background.height - output_image.height) // 2
        background.paste(output_image, (x, y), output_image)
        
        # 6. Сохраняем результат в буфер
        result_bytes = io.BytesIO()
        background.convert("RGB").save(result_bytes, format="JPEG", quality=95)
        result_bytes.seek(0)
        
        # 7. Отправляем готовую карточку
        bot.send_photo(message.chat.id, result_bytes, caption="✅ Готово! Ваша карточка для WB.")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Произошла ошибка: {str(e)}")

@bot.message_handler(content_types=['text'])
def echo_message(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling() 
 
