import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv

headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

url = "https://bamper.by/zchbu/god_2023-2023/store_Y/isused_Y/"
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url=url)
time.sleep(2)

with open("index.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
count = soup.find_all(class_="list-title js-var_iCount")

part_href_url = {}

for item in count:
    count_text = item.text
num = ["0","1","2","3","4","5","6","7","8","9"]
num_page = ""
for char in count_text:
    if char in num:
                num_page = num_page + char
# print(int(num_page))
page = int(int(num_page) / 20) + 1
print(page)
href_count = soup.find_all(class_="brazzers-gallery brazzers-daddy")
n = 1
for item_href in href_count:
    href = "https://bamper.by" + item_href.get("href")
    part_href_url[n] = href
    n += 1
# print(part_href_url)

for number, number_href in part_href_url.items():
    driver.get(url=number_href)
    time.sleep(2)
    with open(f"{number}.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    with open(f"{number}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    """price_obj = soup.find_all("meta", itemprop="price")
    # print (price_obj)
    for item_price in price_obj:
        price = item_price.get("content")
        price = price + " BYN"
    #print(price)

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
    print(marka, model, year, price, number_href)"""

    """artical_obj = soup.find_all("span", class_="data-type f13")
    for item_artical in artical_obj:
        artical = item_artical.text"""
    
    """info_obj = soup.find_all("span", class_="media-heading cut-h-375")
    for item_info in info_obj:
        info = item_info.text.replace("  ","").replace("\n","")"""
    
    benzik_obj = soup.find_all("div", style="font-size: 17px;")
    # print(benzik_obj)
    for item_benzik in benzik_obj:
        benzik = None
        benzik = item_benzik.text.replace("  ","").replace("\n","")
    print(benzik)
    os.remove(f"{number}.html")
os.remove("index.html")
driver.close()
driver.quit()