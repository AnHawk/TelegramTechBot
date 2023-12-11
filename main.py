import telebot
import firebase_admin
from firebase_admin import credentials, firestore

# Ініціалізація Firebase просто в коді
cred = credentials.Certificate("crm-tech-support-firebase-adminsdk-79mmp-a22c9c988f.json")


firebase_admin.initialize_app(cred)
db = firestore.client()

bot = telebot.TeleBot('6662537793:AAHELshKo3xV5zy1BerGyJfCdjnPwp8cG-Y')

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Введіть ваше повідомлення:')
    bot.register_next_step_handler(message, process_message)

def process_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_message = message.text

    # Зберігаємо повідомлення в Firebase
    messages_ref = db.collection('messages')
    messages_ref.add({
        'user_id': user_id,
        'user_name': user_name,
        'message': user_message
    })

    bot.send_message(message.chat.id, 'Повідомлення збережено у Firebase.')

bot.polling(non_stop=True)
