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

service = Service(executable_path="C:\\Dev\\parsingselenium\\chromedriver\\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=service, options=options)

driver.get(url=url)
time.sleep(2)

with open(f"{url}.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)