import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument("start-maximized") # // https://stackoverflow.com/a/26283818/1689770
options.add_argument("enable-automation")#  // https://stackoverflow.com/a/43840128/1689770
#options.add_argument("--headless")#  // only if you are ACTUALLY running headless
options.add_argument("--no-sandbox")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-dev-shm-usage")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-browser-side-navigation")# //https://stackoverflow.com/a/49123152/1689770
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")# //https://stackoverflow.com/a/43840128/1689770
options.add_argument("--enable-javascript")

#options.add_argument(f"--proxy-server={ip}")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})

driver.get('https://bamper.by/personal/')
time.sleep(1)

username_input = driver.find_element(By.NAME, "USER_LOGIN")
username_input.clear()
username_input.send_keys("79119139996")



password_input = driver.find_element(By.NAME, "USER_PASSWORD")
password_input.clear()
password_input.send_keys("Nikita2190")

password_input.send_keys(Keys.ENTER)


with open(f"Заявки на сайте на поиск запчастей.csv", "w", encoding="utf-8") as file_data:
    writer = csv.writer(file_data)

    writer.writerow(
        (
            "МАРКА И МОДЕЛЬ",
            "ИНФО И ЗАПЧАСТЬ",
            "ФИО",
            "НОМЕР ТЕЛЕФОНА",
            "ПОЧТА",
            "НОМЕР И ДАТА ЗАЯВКИ",
            "ФОТОГРАФИЯ"
        )
    )





marka_and_model = ""



for i in range(1,11):
    url = f"https://bamper.by/zayavki/list/?PAGEN_1={i}"
    
    
    driver.get(url=url)
    time.sleep(1)

    with open(f"1.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    with open(f"1.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html.parser')

    marka_and_model = soup.find_all("div", class_="item-list")
    #print(marka_and_model)
    for marka in marka_and_model:
        zapchast_info = ""
        contact = ""
        email = ""
        number_phone = ""
        foto_list = []
        application = ""
        marka = str(marka)
        #print(marka)
        if "/upload/" in marka:
            foto = marka.split('href="')
            #print(foto,"Списко разделенный")
            for text in foto:
                text = str(text)
                #print(text,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                if ("iblock" in text) and (".jpg" in text):
                    href = "https://bamper.by/upload" + str(text[text.find("/iblock") : text.find('target="_blank"')-2])
                    #print(href,"ССылка на фото")
                    print()
                    foto_list.append(href)
                if ("iblock" in text) and (".png" in text):
                    href = "https://bamper.by/upload" + str(text[text.find("/iblock") : text.find('target="_blank"')-2])
                    #print(href,"ССылка на фото")
                    print()
                    foto_list.append(href)

        print()

        

        marka_name = str((marka[marka.find("<span>")+6 : marka.find("/span")-1])).replace("\n","").replace("\r","").replace('"',' ').replace("-",";")
        print(marka_name)
        info = str(marka[marka.find('<h5 class="add-title">') + 22 : marka.find('<span class="hidden">бо')-1]).replace('<br/>',' ').replace("\n",",").replace("\r",",").replace('"',' ').replace("-",";")
        print(info)
        if "fa fa-user" in marka:
            contact = str(marka[marka.find('fa fa-user') + 18 : marka.find('fa fa-phone') - 22]).replace("\n","").replace("\r","").replace('"',' ').replace("-",";")
        if "fa fa-phone" in marka:
            number_phone = str(marka[marka.find('fa fa-phone') + 26 : marka.find('fa fa-envelope') - 22]).replace("\n","").replace("\r","").replace('"',' ').replace("-",";")
        print(contact, "ФИО")
        print(number_phone, "Телефон")
        email = str(marka[marka.find('mailto:') + 7 : marka.find('style="font-weight') - 2]).replace("\n","").replace("\r","").replace('"',' ')
        print(email, "Почта")
        application = marka[marka.find('Заявка') : marka.find(', от ') + 25]
        print(application, "Заявка")
        print(foto_list, "Фотки")
        file = open(f"Заявки на сайте на поиск запчастей.csv", "a", encoding="utf-8", newline='')
        writer = csv.writer(file)

        writer.writerow(
            (
                marka_name,
                info,
                contact,
                number_phone,
                email,
                application,
                foto_list,
            )
        )
        file.close()

        


driver.close()
driver.quit()
    
    