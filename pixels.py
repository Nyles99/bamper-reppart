from PIL import Image
import requests
import os


img = requests.get("https://bamper.by/upload/lk/46c/46c7bea9375d4238baa837fa5b3332f1.jpg")

with open("tmp.jpeg", "wb+") as file:
    file.write(img.content)  # Для сохранения на компьютер

im = Image.open("tmp.jpeg")
pixels = im.load()  # список с пикселями
x, y = im.size  # ширина (x) и высота (y) изображения

white_pix = 0
another_pix = 0

for i in range(x):
    for j in range(y):

        color = pixels[i, j]  # содержит кортеж из нескольких значений цвета, в зависимости от формата изображения

        flag = True  # Флаг, является ли пиксель белым
        for q in range(3):
            # проверка чисто белых пикселей, для оттенков нужно использовать диапазоны
            if pixels[i, j][q] != 255:  # pixels[i, j][q] > 240  # для оттенков
                flag = False

        if flag:
            white_pix += 1
        another_pix += 1

try:
    print(another_pix, white_pix)
    print(round(white_pix / another_pix * 100, 3))
except ZeroDivisionError:
    print("Белых пикселей нет")

os.remove("tmp.jpeg")