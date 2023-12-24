import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv
from PIL import Image, UnidentifiedImageError
import time


input_model = "Vse"
input_number = "Введи один, если не уверен в себе и хочешь обновить марки и модели в списке - "

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

headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


folder_name = input_model + "_fotku_" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

black_list = []

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

number_zapchast = 1
zapchast_list = {}


watermark = Image.open("moe.png")
with open(f"{input_model}_data_bamper.csv", "w", encoding="utf-8") as file_data:
    writer = csv.writer(file_data)

    writer.writerow(
        (
            "АРТИКУЛ",
            "МАРКА",
            "МОДЕЛЬ",
            "ГОД",
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
        )
    )

with open("go_to_catalog.json", encoding="utf-8") as file:
    all_categories_part= json.load(file)

all_href_in_categories = {}

for markah, modelh in all_categories_part.items():
    item_href_categories = f"https://bamper.by/catalog/{markah}-{modelh}/"
    print(item_href_categories)

    req = requests.get(url=item_href_categories, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'html.parser')
    href_part = soup.find_all("a", target="_blank")
    #print(href_part)
    i = 1
    for item in href_part:
        item = str(item)
        #print(item)
        if "zchbu" in item:
            href_in_categories = item[item.find("/zchbu/") : item.find("target=") - 2]
            zapchast = href_in_categories[href_in_categories.find("zapchast") : href_in_categories.find("/marka")]
            #print(zapchast)
            href_in_categories = "https://bamper.by" + href_in_categories + f"god_2012-2023/price-ot_70/store_Y/?ACTION=REWRITED3&FORM_DATA={zapchast}%2Fmarka_{markah}%2Fmodel_{modelh}%2Fgod_2012-2023%2Fprice-ot_70%2Fstore_Y&more=Y&PAGEN_1=" + str(i)
            print(href_in_categories)
            text_in_categories = item[item.find("_blank")+8 : item.find("</a>")]
            
            req = requests.get(url=href_in_categories, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'html.parser')
            href_part = soup.find_all("h5", class_="add-title")
            if href_part != []:
                all_href_in_categories[href_in_categories] = text_in_categories 

with open("page_with_href_zapchast.json", "a", encoding="utf-8") as file:
    json.dump(all_href_in_categories, file, indent=4, ensure_ascii=False)


"""with open("page with href zapchast.json", encoding="utf-8") as file:
    all_href_in_categories= json.load(file)



for item in href_part:
                    item = str(item)
                    href_zapchast = item[item.find("zapchast") : item.find('" target=')]
                    print(href_zapchast)"""