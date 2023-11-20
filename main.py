import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
driver = webdriver.Chrome()

driver.get(url=url)
time.sleep(2)

with open("index.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
count = soup.find_all(class_="list-title js-var_iCount")

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
for item_href in href_count:
    href = "https://bamper.by" + item_href.get("href")
    print(href)
driver.close()
driver.quit()