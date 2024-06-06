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


"""proxy = input("Введи прокси в формате логин:пароль@46.8.158.109:54376 - ")
ip = proxy[proxy.find("@")+1 : ]
print(ip)

proxies = {
    'http': f'{proxy}',
    'https': f'{proxy}'
}"""

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

summa = 0
black_list = []
black_mark = []
spisok_1 = []

"""file1 = open("black-list.txt", "r")
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
#print(black_list)"""

file1 = open("1.txt", "r", encoding="utf-8")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    spisok_1.append(line)
file1.close

url = "https://bamper.by/catalog/modeli/"
driver.get(url=url)
time.sleep(30)
"""req = requests.get(url, headers=headers)
src = req.text
#print(src)
#with open("index.html", "w", encoding="utf-8") as file:
#    file.write(src)
#with open("index.html", encoding="utf-8") as file:
#    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
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

        soup = BeautifulSoup(src, 'html.parser')

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
    json.dump(model_need_list, file, indent=4, ensure_ascii=False)"""        

"""with open('modelu.json', encoding="utf-8") as file:
    model_need_list = json.load(file)"""

zapchast00_1200 = {}
zapchast1200 = {}
null_or_xz = {}
n=1

for url in spisok_1:
    #item_text_model = item_text_model.replace("/","_")
    url_zapchast = str(url)
    #item_href_model = item_href_model[item_href_model.find("catalog/")+8 : len(item_href_model) -1]
    print(url)
    markah = url_zapchast[url_zapchast.find("marka_")+6 : url_zapchast.find("model_")-1 ]
    modelh = url_zapchast[url_zapchast.find("model_")+6 : url_zapchast.find("god_")-1 ]
    #url_zapchast = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2012-2016/price-ot_300/price-do_999/store_y/?more=Y"
    #url_zapchast = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2016-2024/price-ot_1000/store_y/?more=Y"
    #!!!!!!!!!!!!!!!url_zapchast = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2018-2024/price-ot_60/price-do_299/store_y/?more=Y"
    #url_zapchast = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2018-2024/price-ot_1000/store_y/?more=Y"
    #print(url_zapchast)
    try:
        driver.get(url=url_zapchast)
        time.sleep(1)

        with open(f"{1}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open(f"{1}.html", encoding="utf-8") as file:
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
                summa = summa + num_page
                if num_page > 0 and num_page < 1201:
                    page = int(num_page / 20) + 1
                    zapchast00_1200[url_zapchast] = page
                elif num_page > 1200:
                    href_zapchast = []
                    
                    item_href_categories = str(url_zapchast)
                    start_year_start = int(item_href_categories[item_href_categories.find("god_") + 4 : item_href_categories.find("/price-ot_") - 5])
                    end_year_start = int(item_href_categories[item_href_categories.find("god_") + 9 : item_href_categories.find("/price-ot_")])
                    first_year = start_year_start + 5
                    first_part = item_href_categories[ : item_href_categories.find("god_")+ 4]
                    second_part = item_href_categories[item_href_categories.find("/price-ot_") : ]
                    
                    url_zapchast = f"{first_part}{start_year_start}-{first_year}{second_part}"
                    
                    print(url_zapchast)
                    try:
                    #print(url_zapchast)
                        driver.get(url=url_zapchast)
                        time.sleep(1)

                        with open("excample.html", "w", encoding="utf-8") as file:
                            file.write(driver.page_source)

                        with open("excample.html", encoding="utf-8") as file:
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
                                print(num_page)
                                summa = summa + num_page
                                if num_page > 0 and num_page < 1201:
                                    page = int(num_page / 20) + 1
                                    zapchast00_1200[url_zapchast] = page
                                elif num_page > 1200:
                
                                    item_href_categories = str(url_zapchast)
                                    start_year = int(item_href_categories[item_href_categories.find("god_") + 4 : item_href_categories.find("/price-ot_") - 5])
                                    end_year = int(item_href_categories[item_href_categories.find("god_") + 9 : item_href_categories.find("/price-ot_")])
                                    first_part = item_href_categories[ : item_href_categories.find("god_")+ 4]
                                    second_part = item_href_categories[item_href_categories.find("/price-ot_") : ]
                                    for year in range(start_year, (end_year+1)):
                                        url_zapchast = f"{first_part}{year}-{year}{second_part}"
                                        
                                        print(url_zapchast)
                                        try:
                                        #print(url_zapchast)
                                            driver.get(url=url_zapchast)
                                            time.sleep(1)

                                            with open("excample.html", "w", encoding="utf-8") as file:
                                                file.write(driver.page_source)

                                            with open("excample.html", encoding="utf-8") as file:
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
                                                    print(num_page)
                                                    summa = summa + num_page
                                                    if num_page > 0 and num_page < 1201:
                                                        page = int(num_page / 20) + 1
                                                        zapchast00_1200[url_zapchast] = page
                                                    elif num_page > 1200:
                                                        page = int(num_page / 20) + 1
                                                        zapchast1200[url_zapchast] = page
                                                    elif num_page == 0:
                                                        print(url_zapchast, "Страница с нулевым значением нам не нужна")
                                                    else:
                                                        #null_or_xz[url_zapchast] = page
                                                        print("Страница записалась в отдельный список")

                                            os.remove("excample.html")
                                        except Exception:
                                            print(f"Не загрузилась {url_zapchast} - загрузим позже, попробуй обновить вручную в браузере")
                                elif num_page == 0:
                                    zapchast00_1200[url_zapchast] = page
                            
                    except Exception:
                        print(f"Не загрузилась {url_zapchast} - загрузим позже, попробуй обновить вручную в браузере")
                    
                    url_zapchast = f"{first_part}{int(first_year)+1}-{end_year_start}{second_part}"
                    
                    print(url_zapchast)
                    try:
                    #print(url_zapchast)
                        driver.get(url=url_zapchast)
                        time.sleep(1)

                        with open("excample.html", "w", encoding="utf-8") as file:
                            file.write(driver.page_source)

                        with open("excample.html", encoding="utf-8") as file:
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
                                print(num_page)
                                summa = summa + num_page
                                if num_page > 0 and num_page < 1201:
                                    page = int(num_page / 20) + 1
                                    zapchast00_1200[url_zapchast] = page
                                elif num_page > 1200:
                
                                    item_href_categories = str(url_zapchast)
                                    start_year = int(item_href_categories[item_href_categories.find("god_") + 4 : item_href_categories.find("/price-ot_") - 5])
                                    end_year = int(item_href_categories[item_href_categories.find("god_") + 9 : item_href_categories.find("/price-ot_")])
                                    first_part = item_href_categories[ : item_href_categories.find("god_")+ 4]
                                    second_part = item_href_categories[item_href_categories.find("/price-ot_") : ]
                                    for year in range(start_year, (end_year+1)):
                                        url_zapchast = f"{first_part}{year}-{year}{second_part}"
                                        
                                        print(url_zapchast)
                                        try:
                                        #print(url_zapchast)
                                            driver.get(url=url_zapchast)
                                            time.sleep(1)

                                            with open("excample.html", "w", encoding="utf-8") as file:
                                                file.write(driver.page_source)

                                            with open("excample.html", encoding="utf-8") as file:
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
                                                    print(num_page)
                                                    summa = summa + num_page
                                                    if num_page > 0 and num_page < 1201:
                                                        page = int(num_page / 20) + 1
                                                        zapchast00_1200[url_zapchast] = page
                                                    elif num_page > 1200:
                                                        page = int(num_page / 20) + 1
                                                        zapchast1200[url_zapchast] = page
                                                    elif num_page == 0:
                                                        print(url_zapchast, "Страница с нулевым значением нам не нужна")

                                            os.remove("excample.html")
                                        except Exception:
                                            print(f"Не загрузилась {url_zapchast} - загрузим позже, попробуй обновить вручную в браузере")
                            
                    except Exception:
                        print(f"Не загрузилась {url_zapchast} - загрузим позже, попробуй обновить вручную в браузере")
                
                elif num_page == 0:
                    null_or_xz[url_zapchast] = page
                    
        os.remove(f"{1}.html")
    except Exception:
        print(f"Старница {url_zapchast} отвалилась!!!!!!!!!!!!")

with open("null_or_xz.json", "a", encoding="utf-8") as file:
    json.dump(null_or_xz, file, indent=4, ensure_ascii=False)

with open("zapchastot60.json", "a", encoding="utf-8") as file:
    json.dump(zapchast00_1200, file, indent=4, ensure_ascii=False)

with open("zapchastot60.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1200, file, indent=4, ensure_ascii=False)


print(summa)

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие")
