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

proxies = {
    'http': 'http://ZKrvjACdvWKt3Y:Nylesszpg@45.8.125.144:54221',
    'https': 'http://ZKrvjACdvWKt3Y:Nylesszpg@45.8.125.144:54221'
}
input_page = int(input("С какой страницы продолжим?Если сначала - вводи 1 и Enter "))

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
folder_name ="00_1200_year" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

watermark = Image.open("moe.png")
if os.path.exists(f"00_1200_year_data_bamper.csv"):
    print("Папка уже есть")
else:
    with open(f"00_1200_year_data_bamper.csv", "w", encoding="utf-8") as file_data:
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

with open("zapchast00_1200_year.json", encoding="utf-8") as file:
    srazy_parsim = json.load(file)
nomer_str = 0
zapchast_in_black_list = 0
for item_href_categories, number_page in srazy_parsim.items():
    
    item_href_categories = str(item_href_categories)
    markah = item_href_categories[item_href_categories.find("marka")+6:item_href_categories.find("/model_")]
    #print(markah)
    modelh = item_href_categories[item_href_categories.find("model")+6:item_href_categories.find("/god_")]
    diapazon = item_href_categories[item_href_categories.find("god_")+4:item_href_categories.find("/price-ot_70/sto")]
    print(modelh, diapazon)
    for i in range(1, number_page+1):
        item_href_categories = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_{diapazon}/price-ot_70/store_Y/?ACTION=REWRITED3&FORM_DATA=marka_{markah}%2Fmodel_{modelh}%2Fgod_2012-2023%2Fprice-ot_70&2Fstore_Y&more=Y&PAGEN_1={i}"
        nomer_str += 1
        print(f'Номер страницы {nomer_str} - Внимательно')
        print(item_href_categories)
        p = 1
        if nomer_str >= input_page:
            try:
                req = requests.get(url=item_href_categories, headers=headers, proxies=proxies)
                src = req.text
                
                soup = BeautifulSoup(src, 'html.parser')
                href_part = soup.find_all("div", class_="add-image")
                #print(href_part)
                for item in href_part:
                    item = str(item)
                    foto = " "
                    foto = "https://bamper.by" + item[item.find('"tooltip_" src=') + 16 : item.find('title="Нажми,') -2]
                    item = item[item.find("href")+7: item.find("target=") -2]
                    #print(foto)
                    href_to_zapchast = "https://bamper.by/" + item
                    print(href_to_zapchast)
                    number_href_reverse = item[::-1]
                    number_href_reverse_second = number_href_reverse[1:]
                    number_href_reverse = number_href_reverse_second[: number_href_reverse_second.find("/")]
                    name_href = number_href_reverse[::-1]
                    name_href = name_href.replace("*","_").replace('%','_')
                    #print(name_href)
                    num_provider = name_href[: name_href.find("-")]
                    #print(num_provider)
                    if num_provider not in black_list:
                        try:
                            req = requests.get(url=href_to_zapchast, headers=headers, proxies=proxies)
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
                                marka = model_and_year[: model_and_year.find(" ")]
                                model = model_and_year[model_and_year.find(" ")+1 : model_and_year.find(",")]
                                year = model_and_year[model_and_year.find(",")+2 : model_and_year.find("г.")]

                            num_zap = " "
                            num_obj = soup.find_all("span", class_="media-heading cut-h-65")
                            for item_num in num_obj:
                                num_zap = str(item_num.text)
                                num_zap = num_zap.replace("  ","").replace("\n","")
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
                                info = str(item_info.text.replace("  ","").replace("\n",""))
                                info = info.replace(","," ")
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
                            #foto = None
                            #print(foto)<div  style="left: 0px;">
                            if foto != "https://bamper.by/local/templates/bsclassified/images/nophoto_car.png":
                                try:
                                    img = requests.get(foto, proxies=proxies)
                                    img_option = open(f"{folder_name}/{name_href}.png", 'wb')
                                    img_option.write(img.content)
                                    img_option.close
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




                                        foto = "http://95.163.237.225/"+ name_href + ".png"
                                        img = Image.open(f"{folder_name}/{name_href}.png")
                                        #print(foto)
                                        #img = Image.open(f"fotku/{name_href}.png")    
                                        img.paste(watermark,(-272,-97), watermark)
                                        img.paste(watermark,(-230,1), watermark)
                                        img.save(f"{folder_name}/{name_href}.png", format="png")
                                        img_option.close
                                        #os.remove("img.png")
                                        #print(f"{name_href} - неверный формат или ерунда")
                                    except UnidentifiedImageError:
                                            foto = ""
                                            print("Битая фотка")
                                            #os.remove(f"{folder_name}/{name_href}.png")
                                except Exception:
                                    print("Какая-то хуйня с ссылкой на фотографию")
                                    foto = " "
                            else:
                                foto = " "
                                print(name_href , "без фотки")
                                    
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

                            file = open(f"00_1200_year_data_bamper.csv", "a", encoding="utf-8", newline='')
                            writer = csv.writer(file)

                            writer.writerow(
                                (
                                    artical,
                                    marka,
                                    model,
                                    year,
                                    num_zap,
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
                                    foto,
                                    nomer_str
                                )
                            )
                            file.close()
                            #os.remove(f"{num_provider}.html")
                            with requests.request("POST", href_to_zapchast, headers=headers, proxies=proxies) as report:
                                print('report: ', report)
                        except Exception:
                            print("какая-то хуйня с карточкой запчастей")
                    else:
                        print(href_to_zapchast + " находится в black-list, уже "+ str(zapchast_in_black_list) )
                        zapchast_in_black_list += 1
                        #os.remove(f"{number_page}.html")
                        with requests.request("POST", href_to_zapchast, headers=headers, proxies=proxies) as report:
                            print('report: ', report)
                #os.remove(f"{number_page}.html")
            except Exception:
                print("какая-то хуйня со страницей запчастей")    
        else:
            nomer_str += 1
#os.remove("modelu.json")

a = input("Парсинг по  законичил свою работу, нажми 1 и Enter")