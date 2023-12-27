import json
import time
import requests
from bs4 import BeautifulSoup
import os
import csv
from PIL import Image, UnidentifiedImageError
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')

#options.add_argument("--proxy-server=31.204.2.182:9142")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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

folder_name ="no_price" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

watermark = Image.open("moe.png")
with open(f"no_price_data_bamper.csv", "w", encoding="utf-8") as file_data:
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

file1 = open("black-mark.txt", "r", encoding="utf-8")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_mark.append(line)
#print(black_list)

# закрываем файл
file1.close

file1 = open("black-model.txt", "r", encoding="utf-8")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_model.append(line)
#print(black_list)

url = "https://bamper.by/catalog/modeli/"

req = requests.get(url, headers=headers)
src = req.text
#print(src)
#with open("index.html", "w", encoding="utf-8") as file:
#    file.write(src)
#with open("index.html", encoding="utf-8") as file:
#    src = file.read()
soup = BeautifulSoup(src, "lxml")
#print(soup)
marka_need_list = {}
model_need_list = {}


all_mark_models = soup.find_all("h3", class_="title-2")
#print(all_mark_models)
for item in all_mark_models:
    item = str(item)
    item_text = item[item.find("gray")+6 : item.find("/h3")-6]
    item_href_marka = "https://bamper.by"+item[item.find("href=")+6 : item.find("style") - 2]
    #print(item_href_marka, item_text)
    marka_need_list[item_text] = item_href_marka

model_need_list = {}
for item_text_marka, item_href_marka in marka_need_list.items():
    #print(item_text_marka)
    #print(item_href_marka)
    if item_text_marka not in black_mark:
        #print(item_href_marka)
        req = requests.get(url=item_href_marka, headers=headers)
        src = req.text
        #print(src)

        soup = BeautifulSoup(src, "lxml")

        count = soup.find_all("a")
        for item in count:
            item = str(item)
            if "запчасти для <b>" in item:
                #print(item)
                item_text = item[item.find("запчасти для <b>")+16 : item.find("</b> </a>")]
                #print(item_text)
                #if item_text not in black_model:
                item_href_model = "https://bamper.by"+item[item.find("href=")+6 : item.find(">запчасти") - 1]
                #print(item_text)
                if item_text not in black_model:
                    print(item_href_model)
                    markah = item_text[: item_text.find("-")]
                    modelh = item_text[item_text.find("-")+1 :]
                    print(markah, modelh)
                    url_page = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2012-2023/price-do_1/store_Y/?ACTION=REWRITED3&FORM_DATA=marka_{markah}%2Fmodel_{modelh}%2Fgod_2012-2023%2Fprice-do_1%2Fstore_Y&more=Y&PAGEN_1=1"
                    driver.get(url=url_page)
                    time.sleep(1)

                    with open(f"{modelh}.html", "w", encoding="utf-8") as file:
                        file.write(driver.page_source)

                    with open(f"{modelh}.html", encoding="utf-8") as file:
                        src = file.read()

                    soup = BeautifulSoup(src, 'html.parser')

                    count = soup.find_all("h5", class_="list-title js-var_iCount")
                    #print(count)
                    for item in count:
                        item = str(item)
                        if "<b>" in item:
                            #print(item)
                            num_page = item[item.find("<b>")+3: item.find("</b>")]
                            num_page = int(num_page.replace(" ",""))
                    os.remove(f"{modelh}.html")
                    print (markah, modelh, num_page)
    