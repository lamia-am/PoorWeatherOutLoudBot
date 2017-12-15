
# coding: utf-8

import requests
import random
from datetime import datetime, timedelta,timezone

weather_characterization = []
lon, lat = 100000, 100000

def hPa_to_mmHg(value):
    return round(0.75006375541921 * value)

def send_weather_request():
    API_Weather_Key = "046749bb9a8182300f3ec9716d4fdf29"
    url = "http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={APIKEY}".format(
    APIKEY=API_Weather_Key
    )

def point(event, context):
    global weather_characterization
    print(event)
    if is_help_command(event):
        send_message(event["message"]["from"]["id"], help_message())
        return
    try:
        final_message, good_text = main_function(event)
        print("Что не так",good_text, weather_characterization)
        print('phrase',make_search_phrase(good_text, weather_characterization) )
        send_photo(event["message"]["from"]["id"], get_photo_url(make_search_phrase(good_text, weather_characterization)  ))
    except:
        final_message = "Попробуйте набрать еще раз"
    print("weather_characterization:\n",weather_characterization)
    send_message(event["message"]["from"]["id"], final_message)

def send_message(chat_id, text):
    token = "450935191:AAEG8Gw8N3gZPfJCWfe3bmqtmlxjMaorrAg"
    method = "sendMessage"
    url = "https://api.telegram.org/bot{token}/{method}".format(
    token=token,
    method=method
    )
    data = {"chat_id": chat_id,"text": text}
    r = requests.post(url, data = data)
    print(r.json())
    

API_Weather_Key = "046749bb9a8182300f3ec9716d4fdf29"
Url_Weather = "http://api.openweathermap.org/data/2.5/"



def get_current_weather_in_str_many_lines(r):
    global weather_characterization
    s = "Погода сейчас\n"
    s += "Температура: {temp} °C\n".format(
        temp = round(r['main']['temp'])
    )
    s_tmp = ""
    for condition in r['weather']:
        s_tmp += condition['description']+', '
        weather_characterization.append(condition['description'])
    if len(s)>0:
        s_tmp = s_tmp.capitalize()
        s_tmp = s_tmp[:-2]+"\n"
    s += s_tmp
    s += "Ветер: {wind_speed} м/c, {wind_direction}\nДавление: {pressure} мм рт.ст\nВлажность: {humidity}%\n".format(
        wind_speed = round(r['wind']['speed']),
        wind_direction = round(r['wind']['deg']),
        pressure = hPa_to_mmHg(r['main']['pressure']),
        humidity = round(r['main']['humidity'])
    )
    return s

def get_weather_in_str_one_line(r):
    global weather_characterization
    s = "Время: {time}. ".format(time =date_to_str(r['dt'])) 
    s += "Температура: {temp} °C. ".format(
        temp = round(r['main']['temp'])
    )
    s_tmp = ""
    for condition in r['weather']:
        s_tmp += condition['description']+', '
        weather_characterization.append(condition['description'])
    if len(s)>0:
        s_tmp = s_tmp.capitalize()
        s_tmp =s_tmp[:-2]+". "
    s +=s_tmp
    s += "Ветер: {wind_speed} м/c, {wind_direction}. Давление: {pressure} мм рт.ст. Влажность: {humidity}%.\n".format(
        wind_speed = round(r['wind']['speed']),
        wind_direction = round(r['wind']['deg']),
        pressure = hPa_to_mmHg(r['main']['pressure']),
        humidity = round(r['main']['humidity'])
    )
    return s




now_words = {'сейчас', 'сегодня', 'сегодняшний','сегодняшняя','сегодняшней','сегодняшнюю','сегодняшним','сегодняшнего'
               'текущая', 'текущий','текущее','текущим','текущей','текущего','ща'}
words_24h = {'прогноз','прогноза','прогнозу','прогнозы','прогнозом','прогнозе','прогнозам','прогнозами',
                  'метеопрогноз','метеопрогноза','метеопрогнозу','метеопрогнозы','метеопрогнозом',
                  'метеопрогнозе','метеопрогнозам','метеопрогнозами',
                  'предсказание','предсказания',
                  'будет','будем'}
tomorrow_words = {'завтра', 'завтрашний','завтрашняя','завтрашнее','завтрашним','завтрашнего','завтрашней'}
day_after_tomorrow_words = {'послезавтра', 'послезавтрашний','послезавтрашняя','послезавтрашнее',
                            'послезавтрашним','послезавтрашнего','послезавтрашней'}
senseless_words = {'какой','какая','какие','какой','каким','как','что','где','есть','были','была',
                   'погода', 'погодой', 'погоде','погоды','погоду','город',"городе","городу"
                  } 
import re
def text_preprocessing(text):
    text = text.lower()
    text = re.sub(r"[^А-Яа-яA-Za-z0-9-]", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.strip()
    words = text.split()
    clear_words = []
    for word in words:
        if len(word)>=3 and word not in senseless_words or word in {'пн','вт','ср',"чт", "пт","сб","вс","ща"}:
            clear_words.append(word)
    return " ".join(clear_words)

def text_middle_processing(text):
    useless_words = now_words | tomorrow_words | day_after_tomorrow_words | senseless_words | all_days_of_week | words_24h
    words = text.split()
    clear_words = []
    for word in words:
        if word not in useless_words:
            clear_words.append(word)
    return " ".join(clear_words)

def is_week_day(text):
    if len(set(text.split()) & all_days_of_week) != 0:
        return True
    return False

def is_day_after_tomorrow(text):
    if len(set(text.split()) & day_after_tomorrow_words) != 0:
        return True
    return False

def is_tomorrow(text):
    if len(set(text.split()) & tomorrow_words) != 0:
        return True
    return False

def is_24h(text):
    if len(set(text.split()) & words_24h) != 0:
        return True
    return False

def is_now(text):
    if len(set(text.split()) & now_words) != 0:
        return True
    return False


def main_function(telegram_json):
    global lon
    global lat
    global weather_characterization
    weather_characterization = []
    text = telegram_json['message']['text']
    #weather_characterization = []
    #telegram_json ={'update_id': 133885279, 'message': {'message_id': 47, 'from': {'id': 358313097, 'is_bot': False, 
    #                'first_name': 'Sergey', 'last_name': 'Kuliev', 'language_code': 'en'}, 'chat': 
    #                        {'id': 358313097, 'first_name': 'Sergey', 'last_name': 'Kuliev', 'type': 'private'}, 
    #                                'date': 1513310214, 'text': 'rer'}}

    cur_date = datetime.fromtimestamp( telegram_json['message']['date'],
                                     tz =timezone(timedelta(hours=3), 'RTZ 2 (ceia)'))

    text = text_preprocessing(text)
    if is_week_day(text):
        print('week')
        dayOW_id = get_day_of_week(text)
        date_for_request = get_future_date_using_day_of_week(cur_date, dayOW_id)
        text = text_middle_processing(text)
        lon, lat = get_coordinates_of_city_in_good_text(text)
        message_for_post = get_forecast_on_certain_date(date_for_request)
        pass

    elif is_day_after_tomorrow(text):
        text = text_middle_processing(text)
        lon, lat = get_coordinates_of_city_in_good_text(text)
        date_for_request = cur_date + timedelta(days=2)
        message_for_post = get_forecast_on_certain_date(date_for_request)
        

    elif is_tomorrow(text):
        print("tomorrow")
        text = text_middle_processing(text)
        lon, lat = get_coordinates_of_city_in_good_text(text)
        date_for_request = cur_date + timedelta(days=1)
        message_for_post = get_forecast_on_certain_date(date_for_request)
        

    elif is_24h(text):
        print("24h")
        text = text_middle_processing(text)
        lon, lat = get_coordinates_of_city_in_good_text(text)
        message_for_post = get_string_24h_forecast()

    else: # now it means
        print("now")
        text = text_middle_processing(text)
        lon, lat = get_coordinates_of_city_in_good_text(text)
        message_for_post = get_current_weather()
           
    print(text)
    print(weather_characterization)
    print(message_for_post)

    return message_for_post, text 



DaysOW = [{}]*7
DaysOW[0] = {"понедельник","понедельника","понедельнику","понедельником","понедельнике","пн","пнд"}
DaysOW[1] = {"вторник","вторнику","вторником","вторник","вторнике",'вторника',"вт"}
DaysOW[2] = {"среда","среду","средой","среды","среде","ср"}
DaysOW[3] = {"четверг","четверга","четвергу","четвергом","четверге","чт"}
DaysOW[4] = {"пятница","пятницу","пятнице","пятницей","пятницы","пятниц","пт","птн"}
DaysOW[5] = {"суббота","субботе","субботой","субботу","субботы","суббот","сб"}
DaysOW[6] = {"воскресенье","воскресенья","воскресеньем","воскресенью", "вс","вскр"}
all_days_of_week = set()
for day in DaysOW:
    all_days_of_week |= day




def get_day_of_week(text):
    words = set(text.lower().split())
    for day_id in range(7):
        if len(words &DaysOW[day_id])>0:
            return day_id
    return -1




def get_future_date_using_day_of_week(cur_date, dayOW_id):
    cur_id = cur_date.weekday()
    offset = (dayOW_id - cur_id) % 7
    return cur_date + timedelta(days=offset)


def date_to_str(date):
    return "{day}-{month} {hour}:00".format(
        day = date.day,
        month = date.month,
        hour = date.hour,
        #minute = date.minute
    )




def json_to_json_with_datetime(r):
    for id_record in range(len(r['list'])):
        r['list'][id_record]['dt'] = datetime.fromtimestamp( r['list'][id_record]['dt'],tz =timezone(timedelta(hours=3), 'RTZ 2 (ceia)'))
    return r

def compare_dates(date1, date2):
    if date1.day == date2.day and date1.month == date2.month and date1.year == date2.year:
        return True
    return False

API_Weather_Key = "046749bb9a8182300f3ec9716d4fdf29"
Url_Weather = "http://api.openweathermap.org/data/2.5/"

def get_current_weather():
    method = "weather"
    r = requests.get(Url_Weather + method,
                 params={'lon': lon,'lat': lat, 'units': 'metric', 'lang': 'ru', 'APPID': API_Weather_Key})
    rjson = r.json()
    return get_current_weather_in_str_many_lines(rjson)
    
def get_string_24h_forecast():
    method = "forecast"
    r = requests.get(Url_Weather + method,
                 params={'lon': lon,'lat': lat, 'units': 'metric', 'lang': 'ru', 'APPID': API_Weather_Key,'cnt': 8})
    rjson = r.json()
    rjson = json_to_json_with_datetime(rjson)
    s = ""
    for record in rjson['list']:
        s+=get_weather_in_str_one_line(record)
    return s

def get_forecast_on_certain_date(date):
    method = "forecast"
    r = requests.get(Url_Weather + method,
                 params={'lon': lon,'lat': lat, 'units': 'metric', 'lang': 'ru', 'APPID': API_Weather_Key,'cnt': 40})
    rjson = r.json()
    rjson = json_to_json_with_datetime(rjson)
    return pull_out_forecast_on_certain_date(date, rjson)

def pull_out_forecast_on_certain_date(date, r):
    s = ""
    for record in r['list']:
        if compare_dates(date, record['dt']):
            s+=get_weather_in_str_one_line(record)
    return s

def get_coordinates_of_city_in_good_text(text):
    Url_Geocoder = "https://geocode-maps.yandex.ru/1.x/"
    r = requests.get(Url_Geocoder,
                params={'geocode': text,'kind': 'locality', 'format': 'json'})
    rjson = r.json()
    lon, lat = rjson['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
    lon, lat = float(lon), float(lat)
    return lon, lat


import http.client, urllib.parse, json
subscriptionKey = "14c5ae9737164caeaea784ba0da6eeca"

host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/images/search"

def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

def get_photo_url(term):
    print('Searching the Web for: ', term)
    headers, result = BingWebSearch(term)
    rjson = json.loads(result)
    return  rjson['value'][random.randint(0,3)]['contentUrl']
    
def make_search_phrase(good_text, weather_characterization):
    good_text += ' город'
    n = len(weather_characterization) - 1
    if n<0:
        return good_text
    index = random.randint(0, min(3,n))
    return good_text +" "+ weather_characterization[index]

def send_photo(chat_id, photo_url):
    token = "450935191:AAEG8Gw8N3gZPfJCWfe3bmqtmlxjMaorrAg"
    method = "sendPhoto"
    url = "https://api.telegram.org/bot{token}/{method}".format(
    token=token,
    method=method
    )
    data = {"chat_id": chat_id,"photo": photo_url}
    r = requests.post(url, data = data)
    print(r.json())

def is_help_command(event):
    text = event["message"]['text'].lower()
    if text.startswith("/help"):
        return True
    return False

def help_message():
    s = """Вас приветствует погодный бот!
    Я могу показывать текущую в разных уголках мира и прогнозы до 5 дней вперед.
    Везде указано московское время UTC +3.
    Чтобы узнать погоду в интересующий вас день, укажите в запросе слова: 
    сегодня/завтра/послезавтра/понедельник/вторник.. итд + [название города]
    Без уточнения дня, бот покажет текущую погоду.
    Также к ответу бота будет прикреплена картинка, с изображением города во время такой погоды.
    """
    return s

