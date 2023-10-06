import requests
from bs4 import BeautifulSoup
from datetime import datetime


url = "http://www.cbr.ru/scripts/XML_daily.asp?"
#получаем курс валют с сайта ЦБ РФ
def get_course(currency):
    today = datetime.today().strftime("%d/%m/%Y")
    payload = {"date_req": today}
    response = requests.get(url, params=payload)
    html = BeautifulSoup(response.content, "html.parser")
    return str(html.find("valute", {"id" : currency}).value.text)