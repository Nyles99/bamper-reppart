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

driver.close()
driver.quit()