from PIL import Image
import requests
import os

def obrezka(url_foto, name_foto):
    im = requests.get(url_foto)

    with open(name_foto, "wb+") as file:
        file.write(im.content)  # Для сохранения на компьютер

    im = Image.open(name_foto)
    pixels = im.load()  # список с пикселями
    x, y = im.size  # ширина (x) и высота (y) изображения
    min_line_white = []
    n=0
    for j in range(y):
        white_pix = 0
        
        for i in range(x):
            # проверка чисто белых пикселей, для оттенков нужно использовать диапазоны
            if pixels[i, j] == (248,248,248):         # pixels[i, j][q] > 240  # для оттенков
                white_pix += 1
        if white_pix == x:
            n += 1
        #print(white_pix, x, n)

        #print(white_pix)
        min_line_white.append(white_pix)
    left_border = int(min(min_line_white)/2)
    #print(left_border)
    im.crop(((left_border+15), n/2+20, (x-left_border-20), y-(n/2)-20)).save(name_foto, quality=95)
"""try:
    print(another_pix, white_pix)
    print(round(white_pix / another_pix * 100, 3))
except ZeroDivisionError:
    print("Белых пикселей нет")"""

#os.remove("tmp.png")
obrezka("https://bamper.by//upload/lk/49c/b0f9b28fd6cb699abda3f788bc3a3630.jpg", "123.png")