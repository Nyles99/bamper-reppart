import filecmp
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
import urllib.request
import urllib

watermark = Image.open("moe.png")
URL = "https://bamper.by//zapchast_kronshteyn-kryla/2666-98051602/"

url = "https://bamper.by/upload/lk/c44/c449cf6e12a3c7fa7c3b10ebc54d0e0c.jpg"

img = requests.get(url)
img_option = open(f"123.png", 'wb')
img_option.write(img.content)
#img_option.close

im = requests.get(url)
im = Image.open(f"123.png")
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
im.crop(((left_border+15), n/2+20, (x-left_border-20), y-(n/2)-20)).save(f"123.png", quality=95)
img = Image.open(f"123.png")
#img = Image.open(f"fotku/{name_href}.png")    
img.paste(watermark,(-272,-97), watermark)
img.paste(watermark,(-230,1), watermark)
img.save(f"123.png", format="png")
img_option.close



