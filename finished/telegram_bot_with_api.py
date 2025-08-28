import os
import time
import logging
import requests
import dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Загрузка переменных окружения из файла .env
dotenv.load_dotenv()

# Загрузка токена бота из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Необходимо указать TELEGRAM_BOT_TOKEN в переменных окружения")

# Базовый URL для Telegram Bot API
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Функция для получения обновлений (новых сообщений)
def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 30, "offset": offset} if offset else {"timeout": 30}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("result", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении обновлений: {e}")
        return []

# Функция для отправки сообщений
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")

# Обработка команды /start
def handle_start(chat_id):
    send_message(chat_id, "Привет! Я твой телеграм-бот. 🚀\nИспользуй /help, чтобы узнать, что я умею.")

# Обработка команды /help
def handle_help(chat_id):
    send_message(chat_id, "📌 Доступные команды:\n/start - Начать работу с ботом\n/help - Получить список команд")

# Обработка текстовых сообщений
def handle_message(chat_id, text):
    if text.startswith("/"):
        if text == "/start":
            handle_start(chat_id)
        elif text == "/help":
            handle_help(chat_id)
        else:
            send_message(chat_id, "Неизвестная команда. Используй /help для списка команд.")
    else:
        send_message(chat_id, f"Вы написали: {text}")

# Основной цикл бота
def main():
    offset = None
    logging.info("Бот запущен...")
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1  # Обновляем offset для следующего запроса
            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                handle_message(chat_id, text)
        time.sleep(1)  # Пауза между запросами

if __name__ == "__main__":
    main()