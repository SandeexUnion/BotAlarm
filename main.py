import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.ext import Filters

import io
from PIL import Image




# Замените "YOUR_TELEGRAM_BOT_TOKEN" на ваш токен Telegram бота
TOKEN = "7159354718:AAH7QuxMmmcdOfpt3U9cWl_gK9FmL5tZz2Q"
# Замените "YOUR_YANDEX_MAPS_API_KEY" на ваш API-ключ Яндекс.Карт
YANDEX_MAPS_API_KEY = "ecd67f49-eaeb-4cc7-84d4-6c2fd6a7f2f6"
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправьте мне свою геопозицию, чтобы я мог найти ближайшее кафе.')

def get_cafe_location(update: Update, context: CallbackContext) -> None:
    user_location = update.message.location
    latitude = user_location.latitude
    longitude = user_location.longitude

    # Используйте API Google Places для поиска ближайшего кафе
    google_places_api_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=500&type=cafe&key={YANDEX_MAPS_API_KEY}"
    response = requests.get(google_places_api_url)
    cafe_data = response.json()

    if cafe_data["results"]:
        cafe_name = cafe_data["results"][0]["name"]
        cafe_latitude = cafe_data["results"][0]["geometry"]["location"]["lat"]
        cafe_longitude = cafe_data["results"][0]["geometry"]["location"]["lng"]

        # Используйте API Яндекс.Карт для получения изображения карты с отмеченным кафе
        yandex_maps_static_api_url = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&pt={cafe_longitude},{cafe_latitude},pm2dgl~{longitude},{latitude},pm2dgl&z=17&l=map"
        response = requests.get(yandex_maps_static_api_url)

        # Отправка изображения карты с отмеченным кафе пользователю
        update.message.reply_photo(photo=response.content, caption=f"Вот ближайшее кафе \"{cafe_name}\" на карте.")
    else:
        update.message.reply_text("К сожалению, не удалось найти ближайшее кафе.")

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.location, get_cafe_location))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()