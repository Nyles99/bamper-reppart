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
    time.sleep(1)

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
all_zapchast = {}
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
            href_to_zapchast = "https://bamper.by/zchbu/" + item
            #print(item)
            number_href_reverse = item[::-1]
            number_href_reverse_second = number_href_reverse[1:]
            number_href_reverse = number_href_reverse_second[: number_href_reverse_second.find("/")]
            name_href = number_href_reverse[::-1]
            #print(name_href)
            num_provider = name_href[: name_href.find("-")]
            #print(num_provider)
            if num_provider not in black_list:
                zapchast_list[number_zapchast] = href_to_zapchast
                number_zapchast += 1
                #print(number_zapchast, href_to_zapchast)
            else:
                print(href_to_zapchast + " находится в black-list")

        os.remove(f"{zapchast}_{i}.html")
    os.remove(f"{number}.html")

for number_zapchast, item_href_zapchast in zapchast_list.items():
    