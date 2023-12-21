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


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

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
    if item_text_marka not in black_mark:
        print(item_href_marka)
        req = requests.get(url=item_href_marka, headers=headers)
        src = req.text
        #print(src)

        soup = BeautifulSoup(src, "lxml")

        count = soup.find_all("a")
        for item in count:
            item = str(item)
            if "запчасти для <b>" in item:
                item_text = item[item.find("запчасти для <b>")+16 : item.find("</b> </a>")]
                #print(item_text)
                #if item_text not in black_model:
                item_href_model = "https://bamper.by"+item[item.find("href=")+6 : item.find(">запчасти") - 1]
                model_need_list[item_text] = item_href_model
                #print(item_href_model)
                #print(item_text, item_href_model)

with open("modelu.json", "a", encoding="utf-8") as file:
    json.dump(model_need_list, file, indent=4, ensure_ascii=False)        

with open('modelu.json', encoding="utf-8") as file:
    model_need_list = json.load(file)

all_categories_part = {}
n=1
for item_text_model, item_href_model in model_need_list.items():
    if item_text_model not in black_model:
        
        """item_text_model = item_text_model.replace("/","_")
        
        req = requests.get(url=item_href_model, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")

        count = soup.find_all(target="_blank")
        for item in count:
            item = str(item)
            #print(item.find("zchbu"))
            if item.find('zchbu') == 10:
                i = 1
                item_text = item[item.find("_blank")+8 : len(item)-4]
                item_href_categories = "https://bamper.by"+item[item.find("href=")+6 : item.find("target") - 2]+"god_2012-2023/store_Y/?more=Y"
                markah = item_href_categories[item_href_categories.find("marka")+6:item_href_categories.find("/model_")]
                #print(markah)
                modelh = item_href_categories[item_href_categories.find("model")+6:item_href_categories.find("/store_")]
                #print(modelh)
                zapchast = item_href_categories[item_href_categories.find("zchbu")+6:item_href_categories.find("/marka_")]
                #print(zapchast)
                item_href_categories = "https://bamper.by/zchbu/"+zapchast+"/marka_"+markah+"/model_"+modelh+ \
                "/god_2012-2023/store_Y/?ACTION=REWRITED3&FORM_DATA="+ zapchast+ "%2Fmarka_" + \
                markah + "%2Fmodel_" + modelh +"%2Fgod_2012-2023%2Fstore_Y&PAGEN_1="+str(i)
                req = requests.get(url=item_href_categories, headers=headers)
                src = req.text
                soup = BeautifulSoup(src, "lxml")
                count_text = soup.find("h4").text
                count = soup.find_all("div", class_="seo1")
                #print(count)
                if "Объявлений не найдено" not in count_text:               
                    all_categories_part[n] = item_href_categories
                    print(n, item_href_categories)
                    n += 1
                    while count == []:
                        i += 1
                        item_href_categories = "https://bamper.by/zchbu/"+zapchast+"/marka_"+markah+"/model_"+modelh+ \
                        "/god_2012-2023/store_Y/?ACTION=REWRITED3&FORM_DATA="+ zapchast+ "%2Fmarka_" + \
                        markah + "%2Fmodel_" + modelh +"%2Fgod_2012-2023%2Fstore_Y&PAGEN_1="+str(i)
                        req = requests.get(url=item_href_categories, headers=headers)
                        src = req.text
                        soup = BeautifulSoup(src, "lxml")
                        count = soup.find_all("div", class_="seo1")
                        if count == []:
                            all_categories_part[n] = item_href_categories
                            n += 1
                            print(n, item_href_categories)
os.remove("modelu.json")"""           
           

#with open("categories.json", "a", encoding="utf-8") as file:
    #json.dump(all_categories_part, file, indent=4, ensure_ascii=False)