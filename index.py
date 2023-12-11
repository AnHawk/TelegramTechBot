import requests
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен вашого бота
TELEGRAM_BOT_TOKEN = "API:6662537793:AAHELshKo3xV5zy1BerGyJfCdjnPwp8cG-Y"

# Дані Firebase
FIREBASE_API_KEY = "AIzaSyBRsPXwZqwcY4FYW-NttN78lyjg_sDkAiY"
FIREBASE_AUTH_DOMAIN = "crm-tech-support.firebaseapp.com"
FIREBASE_PROJECT_ID = "crm-tech-support"
FIREBASE_STORAGE_BUCKET = "crm-tech-support.appspot.com"
FIREBASE_MESSAGING_SENDER_ID = "1036703644603"
FIREBASE_APP_ID = "1:1036703644603:web:5d59ea90b9ab0ff452a29e"

# URL для взаємодії з Firebase Realtime Database
FIREBASE_DB_URL = f"https://{FIREBASE_PROJECT_ID}.firebaseio.com/messages.json?auth={FIREBASE_API_KEY}"

# Функція для обробки команди /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Ваш бот готовий до роботи!')

# Функція для обробки повідомлень від користувачів
def handle_message(update: Update, context: CallbackContext) -> None:
    # Отримання тексту повідомлення від користувача
    user_message = update.message.text

    # Відправлення повідомлення до Firebase
    firebase_data = {"message": user_message}
    response = requests.post(FIREBASE_DB_URL, json=firebase_data)

    if response.status_code == 200:
        update.message.reply_text('Повідомлення успішно додано до колекції "messages" в БД Firebase!')
    else:
        update.message.reply_text('Виникла помилка при додаванні повідомлення до БД Firebase.')

# Основна функція для запуску бота
def main() -> None:
    # Створення об'єкта бота
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(bot=bot)

    # Додавання обробників команд та повідомлень
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
