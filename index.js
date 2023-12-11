const TelegramBot = require('node-telegram-bot-api');
const admin = require('firebase-admin');

// Replace with your Firebase configuration
const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_API_KEY",
  authDomain: "YOUR_FIREBASE_AUTH_DOMAIN",
  projectId: "YOUR_FIREBASE_PROJECT_ID",
  storageBucket: "YOUR_FIREBASE_STORAGE_BUCKET",
  messagingSenderId: "YOUR_FIREBASE_MESSAGING_SENDER_ID",
  appId: "YOUR_FIREBASE_APP_ID",
  measurementId: "YOUR_FIREBASE_MEASUREMENT_ID"
};

// Replace with your Telegram Bot token
const botToken = 'YOUR_TELEGRAM_BOT_TOKEN';

// Initialize Firebase
admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  databaseURL: `https://${firebaseConfig.projectId}.firebaseio.com`
});

const bot = new TelegramBot(botToken, { polling: true });

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const messageText = msg.text;

  // Send the message to Firebase
  try {
    await sendMessageToFirebase(chatId, messageText);
    bot.sendMessage(chatId, 'Ваше повідомлення було доставлено до Firebase');
  } catch (error) {
    console.error('Помилка відправки повідомлення до Firebase:', error);
    bot.sendMessage(chatId, 'Виникла помилка при відправці повідомлення до Firebase');
  }
});

async function sendMessageToFirebase(chatId, message) {
  const db = admin.firestore();
  const messagesRef = db.collection('messages');

  // Add the message to the Firebase collection
  await messagesRef.add({
    chatId: chatId,
    message: message,
    timestamp: admin.firestore.FieldValue.serverTimestamp()
  });
}
