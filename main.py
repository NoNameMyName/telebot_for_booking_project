# 5343530951:AAEex6DokHg91DHSbBMtJVCHR7t9eeMq6_A
# @smart_bot_22_bot
# smart_test_bot_22_bot
import requests

from telebot import (
    TeleBot,
    types
)

bot = TeleBot("5343530951:AAEex6DokHg91DHSbBMtJVCHR7t9eeMq6_A")

response = requests.get(url="http://127.0.0.1:8000/hotels/api/show_hotels/").json()

cities = []
hotels = []


def get_city_names(elem):
    return elem.get("city")


def get_cities():
    for i in response:
        city_to_add = get_city_names(i)
        if city_to_add not in cities:
            cities.append(city_to_add)
    return cities


def get_hotel_names(elem, user_city):
    if get_city_names(elem) == user_city:
        return elem.get("title")


def get_hotels_for_user(user_city):
    for i in response:
        hotels_to_add = get_hotel_names(i, user_city)
        if hotels_to_add is not None:
            hotels.append(hotels_to_add)
    return hotels


get_cities()


@bot.message_handler(commands=["start", "help"])
def start_help_handler(message: types.Message):
    if message.text == "/start":
        hotels.clear()
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Hello, {message.from_user.first_name}\n"
                 f"What city do you want to stay in from this list?\n"
                 f"{cities}"
        )
    if message.text == "/help":
        bot.send_message(
            chat_id=message.chat.id,
            text=f"This bot can help you to search and book hotel if u want to start sent /start"
        )
# TODO: Write help-command help_hendler(/help)
#  Functional: Bot should connect to Django and get all hotels for user city
# TODO: Read about pyTelegramBotApi


@bot.message_handler(func=lambda m: True)
def echo_all(message: types.Message):
    info = {}
    info["chat_i"] = message.chat.id
    info["msg_id"] = message.id
    info["user_id"] = message.from_user.id
    info["user_first_name"] = message.from_user.first_name
    print(f"{info}")
    if message.text in cities:
        hotels.clear()
        user_city = message.text
        get_hotels_for_user(user_city)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'U choosed: {user_city}\nHotels for u: {hotels}'
        )
    elif message.text not in cities:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"We don`t work in this city or you didn`t correct write the city"
        )
    # if message.text in hotels:
    #     bot.send_message(
    #         chat_id=message.chat.id,
    #         text=f"Do you want to booking the room?"
    #     )
    if message.text == "Data":
        bot.send_message(
            chat_id=message.chat.id,
            text=f"{response}"
        )

    # bot.reply_to(message, message.text)


bot.infinity_polling()
