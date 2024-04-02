from openpyxl import load_workbook
import csv
import json
import time
import requests
from bs4 import BeautifulSoup
import os

input_name = input("Введи точное имя файла без xlsx и нажми ENTER ")
book = load_workbook(f"{input_name}.xlsx")
sheet = book["Лист1"]

with open(f"{input_name}.csv", "w", encoding="utf-8") as file_data:
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
with open("marka_model.json", encoding="utf-8") as file:
    srazy_parsim = json.load(file)
mod_list = []
mar_list = []
    #mod_list.append[mod]
    #mar_list.append[mar]
for i in range(2, 200000):
    
    artical = sheet["A"+ str(i)].value
    marka = str(sheet["B"+ str(i)].value)
    marka = marka.replace('"',"")
    
    for mod, mar in srazy_parsim.items():
        if marka in mar:
            marka = mar
    model = str(sheet["C"+ str(i)].value)
    models = model.split()
    for m in models:
        for mod, mar in srazy_parsim.items():
            if m in mod and marka in mar:
                model = mod
    model = model.replace('"',"").replace(','," ")           
    
    year = sheet["D"+ str(i)].value
    for n in range (1980, 2024):
        if str(n) in str(year):
            year =n
    year = str(year).replace('"',"")

    num_zap = str(sheet["E"+ str(i)].value)
    num_zap = num_zap.replace('"','').replace("далее","").replace(","," ").rstrip()
    href_to_zapchast = sheet["F"+ str(i)].value
    fuel = sheet["G"+ str(i)].value
    volume = sheet["H"+ str(i)].value
    engine = sheet["I"+ str(i)].value
    transmission = sheet["H"+ str(i)].value
    car_body = sheet["K"+ str(i)].value
    name_part = str(sheet["L"+ str(i)].value)
    name_part =name_part.replace('"',"")
    info = sheet["M"+ str(i)].value
    order = sheet["N"+ str(i)].value
    price = sheet["O"+ str(i)].value
    status = sheet["P"+ str(i)].value
    foto = sheet["Q"+ str(i)].value
    nomer_str = sheet["R"+ str(i)].value


    file = open(f"{input_name}.csv", "a", encoding="utf-8", newline='')
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
1