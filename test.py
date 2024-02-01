import json
import time
import requests
from bs4 import BeautifulSoup
import os
import csv
from PIL import Image, ImageFile, UnidentifiedImageError
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait




ImageFile.LOAD_TRUNCATED_IMAGES = True
headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


summa = 0
black_list = []
black_mark = []
black_model = []

file1 = open("black-list.txt", "r")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_list.append(line)
#print(black_list)
# закрываем файл
file1.close

# Адрес сайта, с которого мы будем получать данные
url_byn = "https://www.google.com/search?q=курс+доллара+к+белорусскому+рублю"
    
# Получаем содержимое страницы
response = requests.get(url_byn)
    
# Создаем объект BeautifulSoup для парсинга HTML-разметки
soup = BeautifulSoup(response.content, 'html.parser')
    
# Получаем элемент с курсом валюты
result = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text()
    
# Возвращаем курс валюты как число
usd_byn =  float(result.replace(",", ".")[:4])
print("На сегодня 1USD = "+ str(usd_byn) + "BYN")
folder_name ="00_1200_" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

watermark = Image.open("moe.png")
if os.path.exists(f"00_1200_data_bamper.csv"):
    print("Папка уже есть")
else:
    with open(f"00_1200_data_bamper.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
                "АРТИКУЛ",
                "МАРКА",
                "МОДЕЛЬ",
                "ГОД",
                "НОМЕР ЗАПЧАСТИ",
                "ССЫЛКА НА ЗАПЧАСТЬ",
                "ТОПЛИВО",
                "ОБЪЕМ",
                "ТИП ДВИГАТЕЛЯ",
                "КОРОБКА",
                "ТИП КУЗОВА",
                "ЗАПЧАСТЬ",
                "ОПИСАНИЕ",
                "ПОД ЗАКАЗ",
                "ЦЕНА",
                "НОВАЯ",
                "ФОТО",
                "СТРАНИЦА окончания",
            )
        )



zapchast_in_black_list = 0

item_href_categories = "https://bamper.by/zapchast_fara-pravaya/13735-105473294/"    

print(item_href_categories)

req = requests.get(url=item_href_categories, headers=headers)
#print(req)
src = req.text
soup = BeautifulSoup(src, 'html.parser')
href_part = soup.find_all("div", class_="add-image")
print(href_part)

        
req = requests.get(url=item_href_categories, headers=headers)
src = req.text

soup = BeautifulSoup(src, 'html.parser')
price_obj = soup.find_all("meta", itemprop="price")
#print (price_obj)
#if price_obj != []:
for item_price in price_obj:
    price = item_price.get("content").replace(" ","")
    price = round(float(price)/usd_byn)
marka_obj = soup.find_all("span", itemprop="name")
for item_marka in marka_obj:
    all_title_name = str(item_marka)
    string = all_title_name[all_title_name.find("<b>") + 1 : ]
    number_b = string.find('</b>')
    name_part = string[2:number_b]
    model_and_year = string[string.find(' к ')+3 :]
    marka = model_and_year[: model_and_year.find(" ")].replace(",","").replace('"',"")
    model = model_and_year[model_and_year.find(" ")+1 : model_and_year.find(",")].replace(",","").replace('"',"")
    year = model_and_year[model_and_year.find(",")+2 : model_and_year.find("г.")].replace(",","").replace('"',"")

num_zap = " "
num_obj = soup.find_all("span", class_="media-heading cut-h-65")
for item_num in num_obj:
    num_zap = str(item_num.text).replace("  ","").replace('"',"")
    num_zap = num_zap.replace(",","").replace("\n","")
print(num_zap)


artical_obj = soup.find_all("span", class_="data-type f13")
for item_artical in artical_obj:
    artical = item_artical.text

        
#print(marka, model, year, price, number_href)

            
order = " "
status = "Б/у"
info = " "
info_obj = soup.find_all("span", class_="media-heading cut-h-375")
for item_info in info_obj:
    print(item_info, "строка")
    info = str(item_info.text.replace("  ","").replace("\n",""))
    info = info.replace(","," ").replace('"',' ')
    info = info.replace("\r","")
    info_lower = info.lower()
    
    if "ПОД ЗАКАЗ" in info:
        order = "ПОД ЗАКАЗ"
    # print(info)
    if "новый" in info_lower:
        status = "Новая"
    elif "новая" in info_lower:
        status = "Новая"
    elif "новые" in info_lower:
        status = "Новые"

print(info)
#print(status)
#print(order)        
#print(info)
#foto = None
#print(foto)<div  style="left: 0px;">
        
benzik_obj = soup.find_all("div", style="font-size: 17px;")
fuel = " "
transmission = " "
engine = " "
volume = " "

car_body = " "
# print(benzik_obj)


for item_benzik in benzik_obj:
    benzik = " "
    benzik = item_benzik.text.replace("  ","").replace("\n","")
    if "л," in benzik:
        volume = benzik[benzik.find("л,") - 5 : benzik.find("л,") + 1]
    if "бензин" in benzik:
        fuel = "бензин"
    elif "дизель" in benzik:
        fuel = "дизель"
    elif "электро" in benzik:
        fuel = "электро"
    elif "гибрид" in benzik:
        fuel = "гибрид"
    if "TSI" in benzik:
        engine = "TSI"
    elif "TDI" in benzik:
        engine = "TDI"
    elif "MPI" in benzik:
        engine = "MPI"
    elif "CRDI" in benzik:
        engine = "CRDI"
    if "АКПП" in benzik:
        transmission = "АКПП"
    elif "МКПП" in benzik:
        transmission = "МКПП"
    elif "вариатор" in benzik:
        transmission = "вариатор"
    if "седан" in benzik:
        car_body = "седан"
    elif "хетчбек" in benzik:
        car_body = "хетчбек"
    elif "внедорожник" in benzik:
        car_body = "внедорожник"
    elif "универсал" in benzik:
        car_body = "универсал"
    elif "кабриолет" in benzik:
        car_body = "кабриолет"
    elif "микроавтобус" in benzik:
        car_body = "микроавтобус"
    elif "пикап" in benzik:
        car_body = "пикап" 
#print(volume, fuel, transmission, engine, car_body)
#print(benzik)

file = open(f"00_1200_data_bamper.csv", "a", encoding="utf-8", newline='')
writer = csv.writer(file)

writer.writerow(
    (
        artical,
        marka,
        model,
        year,
        num_zap,
        num_zap,
        fuel,
        volume,
        engine,
        transmission,
        car_body,
        name_part,
        info,
        order,
        price,
        status,
        status,
        0
    )
)
file.close()   
