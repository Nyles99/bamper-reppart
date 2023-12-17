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


"""headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

url = "https://bamper.by/catalog/modeli/"

req = requests.get(url, headers=headers)
src = req.text
#print(src)
with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)
name_part= []
with open("index.html", encoding="utf-8") as file:
    src = file.read()
f = open( '123.txt', 'w', encoding="utf-8" )
soup = BeautifulSoup(src, "lxml")
all_mark_models = soup.find_all("div", class_="row")
for item in all_mark_models:
    item = str(item.text).replace("  ","").replace("\n\n","")
    # print(item)
    f.write("%s\n" % item)
f.close()
with open('123.txt', 'r', encoding="utf-8" ) as file:
    for line in file:
        if "запчасти" in line:
            line = line.replace("\n","").replace("запчасти для","")
            name_part.append(line)
#print(name_part)

f = open( '1234.txt', 'w', encoding="utf-8" )
for item in name_part:
    f.write("%s\n" % item)
f.close()""" 

input_model = input("Здорово, заебал, вводи марку авто,  запчасти которой хочешь спиздить  -  ")

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

url = "https://bamper.by/catalog/modeli/"
black_mark = []
black_model = []

folder_name = input_model + "_fotku_" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

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

# закрываем файл
file1.close

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


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('excludeSwitches', ['enable-automation'])
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
#options.add_argument("--proxy-server=31.204.2.182:9142")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})

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

driver.get(url=url)
time.sleep(2)

with open("index.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, 'html.parser')
marka_need_list = {}
count = soup.find_all("h3", class_="title-2")
for item in count:
    item = str(item)
    item_text = item[item.find("gray")+6 : item.find("/h3")-6]
    if item_text not in black_mark:
        item_href_marka = "https://bamper.by"+item[item.find("href=")+6 : item.find("style") - 2]
        marka_need_list[item_text] = item_href_marka
        #print(item_text)
os.remove("index.html")

for item_text_marka, item_href_marka in marka_need_list.items():
    if item_text_marka == input_model:

        driver.get(url=item_href_marka)
        time.sleep(1)

        with open(f"{item_text_marka}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open(f"{item_text_marka}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')
        model_need_list = {}
        count = soup.find_all("a")
        for item in count:
            item = str(item)
            if "запчасти для <b>" in item:
                item_text = item[item.find("запчасти для <b>")+16 : item.find("</b> </a>")]
                #print(item_text)
                if item_text not in black_model:
                    item_href_model = "https://bamper.by"+item[item.find("href=")+6 : item.find(">запчасти") - 1]
                    model_need_list[item_text] = item_href_model
                    #print(item_text, item_href_model)
        os.remove(f"{item_text_marka}.html")

all_categories_part = {}
n=1
for item_text_model, item_href_model in model_need_list.items():
    print(item_href_model)
    driver.get(url=item_href_model)
    time.sleep(5)

    with open(f"{item_text_model}.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    with open(f"{item_text_model}.html", encoding="utf-8") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, 'html.parser')
    
    count = soup.find_all(target="_blank")
    for item in count:
        item = str(item)
        #print(item.find("zchbu"))
        if item.find('zchbu') == 10:
            item_text = item[item.find("_blank")+8 : len(item)-4]
            item_href_categories = "https://bamper.by"+item[item.find("href=")+6 : item.find("target") - 2]+"store_Y/"
            all_categories_part[n] = item_href_categories
            #print(n)
            n += 1
    os.remove(f"{item_text_model}.html")

#print(all_categories_part)

for number, item_href_categories in all_categories_part.items():
    #print(number, item_href_categories)
    driver.get(url=item_href_categories)
    time.sleep(1)

    with open(f"{number}.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    with open(f"{number}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html.parser')
    count = soup.find("h5", class_="list-title js-var_iCount")
    #print(count)
    #Проверка сколько страниц с фильтром!!!!!!!!!!!!!!!!!!!!!!
    for item in count:
        item = str(item)
        if "<b>" in item:
            #print(item)
            num_page = int(item[3:item.find("</b>")])
    if num_page > 20:
        page = int(num_page / 20) + 1
    else:
        page = 1
    #print(page)
    markah = item_href_categories[item_href_categories.find("marka")+6:item_href_categories.find("/model_")]
    #print(markah)
    modelh = item_href_categories[item_href_categories.find("model")+6:item_href_categories.find("/store_")]
    #print(modelh)
    zapchast = item_href_categories[item_href_categories.find("zchbu")+6:item_href_categories.find("/marka_")]
    #print(zapchast)
    #Уровень страница с запчастями!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for i in range(1,page+1):
        url_page = "https://bamper.by/zchbu/"+zapchast+"/marka_"+markah+"/model_"+modelh+"/store_Y/?ACTION=REWRITED3&FORM_DATA="+ zapchast+ "%2Fmarka_" + markah + "%2Fmodel_" + modelh +"%2Fstore_Y&PAGEN_1="+str(i)
        #print(url_page)
        driver.get(url=url_page)
        time.sleep(1)

        with open(f"{zapchast}_{i}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open(f"{zapchast}_{i}.html", encoding="utf-8") as file:
            src = file.read()

        soupp = BeautifulSoup(src, 'html.parser')

        href_part = soupp.find_all("a",target="_blank", class_="brazzers-gallery brazzers-daddy")
        for item in href_part:
            item = item.get("href")
            href_to_zapchast = "https://bamper.by/" + item
            #print(item)
            number_href_reverse = item[::-1]
            number_href_reverse_second = number_href_reverse[1:]
            number_href_reverse = number_href_reverse_second[: number_href_reverse_second.find("/")]
            name_href = number_href_reverse[::-1]
            #print(name_href)
            num_provider = name_href[: name_href.find("-")]
            #print(num_provider)
            if num_provider not in black_list:
                wait = WebDriverWait(driver, 7200)
                driver.get(url=href_to_zapchast)
                wait.until(EC.element_to_be_clickable((By.ID, "wrapper")))
                with open(f"{name_href}.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)

                with open(f"{name_href}.html", encoding="utf-8") as file:
                    src = file.read()

                soup = BeautifulSoup(src, 'html.parser' )

                price_obj = soup.find_all("meta", itemprop="price")
                #print (price_obj)
                if price_obj != []:
                    for item_price in price_obj:
                        price = item_price.get("content").replace(" ","")
                        price = round(float(price)/usd_byn)
                else:
                    price = 100000000
                print(price)
                if price > 20:
                    if price == 100000000:
                        price = "Цена не указана"

                    marka_obj = soup.find_all("span", itemprop="name")
                    for item_marka in marka_obj:
                        all_title_name = str(item_marka)
                        string = all_title_name[all_title_name.find("<b>") + 1 : ]
                        number_b = string.find('</b>')
                        name_part = string[2:number_b]
                        model_and_year = string[number_b+8 :]
                        marka = model_and_year[: model_and_year.find(" ")]
                        model = model_and_year[model_and_year.find(" ")+1 : model_and_year.find(",")]
                        year = model_and_year[model_and_year.find(",")+2 : model_and_year.find("г.")]
                    if int(year) > 2011:

                        artical_obj = soup.find_all("span", class_="data-type f13")
                        for item_artical in artical_obj:
                            artical = item_artical.text

                        
                        #print(marka, model, year, price, number_href)

                            
                        order = None
                        status = "Б/у"
                        info = None
                        info_obj = soup.find_all("span", class_="media-heading cut-h-375")
                        for item_info in info_obj:
                            info = item_info.text.replace("  ","").replace("\n","")
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
                        #print(status)
                        #print(order)        
                        #print(info)
                        foto = None
                        
                        image_obj = str(soup.find("img", class_="fotorama__img"))
                        # print(image_obj)
                        foto = "https://bamper.by" + image_obj[image_obj.find("src=")+5 : image_obj.find("style=")-2]
                        #print(foto)
                        if foto != "https://bamper.by/local/templates/bsclassified/images/nophoto_car.png":
                            img = requests.get(foto)
                            img_option = open(f"{folder_name}/{name_href}.png", 'wb')
                            img_option.write(img.content)
                            #img_option.close

                            im = requests.get(foto)

                            with open(f"{folder_name}/{name_href}.png", "wb+") as file:
                                file.write(im.content)  # Для сохранения на компьютер
                            try:
                                im = Image.open(f"{folder_name}/{name_href}.png")
                                pixels = im.load()  # список с пикселями
                                x, y = im.size  # ширина (x) и высота (y) изображения
                                min_line_white = []
                                n=0
                                for j in range(y):
                                    white_pix = 0
                    
                                    for m in range(x):
                                        # проверка чисто белых пикселей, для оттенков нужно использовать диапазоны
                                        if pixels[m, j] == (248,248,248):         # pixels[i, j][q] > 240  # для оттенков
                                            white_pix += 1
                                    if white_pix == x:
                                        n += 1
                                    #print(white_pix, x, n)

                                    #print(white_pix)
                                    min_line_white.append(white_pix)
                                left_border = int(min(min_line_white)/2)
                                #print(left_border)
                                im.crop(((left_border+15), n/2+20, (x-left_border-20), y-(n/2)-20)).save(f"{folder_name}/{name_href}.png", quality=95)





                                img = Image.open(f"{folder_name}/{name_href}.png")
                                print(foto)
                                #img = Image.open(f"fotku/{name_href}.png")    
                                img.paste(watermark,(-272,-97), watermark)
                                img.paste(watermark,(-230,1), watermark)
                                img.save(f"{folder_name}/{name_href}.png", format="png")
                                img_option.close
                                #os.remove("img.png")
                                #print(f"{name_href} - неверный формат или ерунда")
                            except UnidentifiedImageError:
                                foto = "Битая фотка"
                                print("Битая фотка")
                        else:
                            foto = "Нет фотографии"
                            print(name_href , "без фотки")
                                
                        benzik_obj = soup.find_all("div", style="font-size: 17px;")
                        fuel = None
                        transmission = " "
                        engine = " "
                        volume = None
                        car_body = None
                        # print(benzik_obj)
                        for item_benzik in benzik_obj:
                            benzik = None
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

                        file = open(f"{input_model}_data_bamper.csv", "a", encoding="utf-8", newline='')
                        writer = csv.writer(file)

                        writer.writerow(
                            (
                                artical,
                                marka,
                                model,
                                year,
                                href_to_zapchast,
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
                                foto
                            )
                        )
                        file.close()
                        os.remove(f"{name_href}.html")
                    else:
                        print("запчасть старенькая,а нам нужна молоденькая")
                        os.remove(f"{name_href}.html")
                else:
                    os.remove(f"{name_href}.html")
                    print(f'{name_href} меньше 20$, цена запчасти = {price}')
                """else:
                    print(href_to_zapchast + "цена по запросу, ахуели?)")
                    os.remove(f"{name_href}.html")"""
            
            
            else:
                print(href_to_zapchast + " находится в black-list")

        os.remove(f"{zapchast}_{i}.html")
    os.remove(f"{number}.html")
os.remove(f"index.html")

input(f"Парсинг по {input_model} законичил свою работу, нажми Enter")
