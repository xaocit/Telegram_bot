import telebot
import datetime
import requests
from config import tg_bot_token, open_weather_token
from course import get_course
from wiki import get_wiki_article


#Токен
bot = telebot.TeleBot(tg_bot_token)

@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Привет! Я бот!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    msg = message.text.lower()
    chat_id = message.chat.id
    try:
        if msg == "/currency":
            response =   "\n {0} рублей за 1 доллар \n".format(get_course("R01235"))
            response +=  " {0} рублей за 1 евро \n".format(get_course("R01239"))
            response +=  " {0} рублей за 10 юаней \n".format(get_course("R01375"))
            response +=  " {0} рублей за 1 фунт \n".format(get_course("R01035"))
            bot.send_message(chat_id, response)
        
        elif msg == "/wiki":
            get_message_to_wiki(message)

        elif msg == "/weather":
            get_message_to_weather(message)

        else:
            response = "Неизвестная команда"
            bot.send_message(chat_id, response)
    except telebot.apihelper.ApiTelegramException:
        response = "Произошла ошибка при отправке сообщения"
        bot.send_message(chat_id, response)
   
def get_message_to_wiki(message):
    bot.send_message(message.chat.id, 'Отлично! Напиши мне запрос')
    bot.register_next_step_handler(message, get_wiki)

def get_wiki(message):
    article = message.text.lower()
    response = get_wiki_article(article)
    bot.send_message(message.chat.id, response)

def get_message_to_weather(message):
    bot.send_message(message.chat.id, "Отлично! Пришли мне свой город(Название)")
    bot.register_next_step_handler(message, get_weather)

@bot.message_handler()
def get_weather(message: telebot.types.Message):
    code_to_smile = {
        "Clear": "Ясно",
        "Clouds" : "Облачно",
        "Rain": "Дождь",
        "Thunderstorm": "Гроза",
        "Snow": "Снег",
        "Mist" : "Туман",
    }
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()

        city = data["name"]
        country = data["sys"]["country"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            bot.send_message(message.chat.id, "Неизвестная погода!!!")
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_time_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        bot.send_message(message.chat.id, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                         f"Погода в городе: {city}, {country}\n"
                         f"Температура: {cur_weather} {wd}\n"
                         f"Влажность: {humidity} Давление: {pressure} мм. рт. ст.\n Ветер: {wind} м/c\n"
                         f"Восход: {sunrise_time}\n Закат: {sunset_time}\n Продолжительность дня: {length_time_of_day}")
    except:
        bot.send_message(message.chat.id, "Проверьте название города!!!")
        get_message_to_weather(message)
    


bot.polling(none_stop=True)
