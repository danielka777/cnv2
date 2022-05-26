# -*- coding: utf-8 -*-
"""функции.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/danielka777/cnv2/blob/main/%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B8.ipynb

## **Содержание:**

[1. Загрузка библиотек](#load_bibl)

[2. Алгоритмы конвертации](#algs)
*   [Алгоритм прямой видимости](#nvg)
*   [Горизонтальный алгоритм](#hvg)
*   [Скользящее окно для nvg](#snvg)
*   [Скользящее окно для hvg](#shvg)

[3. Функция для работы с пользователем](#user)

[4. Интерфейс для работы](#workk)

### 1. Загрузка библиотек<a name="load_bibl"></a>
"""

# импортируем необходимые библиотеки
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from google.colab import files
import io

import time
from tqdm import tqdm

"""### 2. Алгоритмы конвертации<a name="algs"></a>

#### Алгоритм прямой видимости<a name="nvg"></a>
"""

def nvg(y):  # на вход массив значений
     #на выходе отсортированый массив(target source)
    source_target = []
    for i in tqdm(range(len(y) - 1)):
        source_target.append([i + 1, i + 2])
        for j in range(i + 2, len(y)):
            flg = False
            for k in range(i + 1, j):
                if y[k] < y[j] + ((y[i] - y[j]) * ((j - k) / (j - i))):
                    flg = True
                else:
                    flg = False
                    break

            if flg:
                source_target.append([i + 1, j + 1])
                
    return source_target

"""#### Горизонтальный алгоритм<a name="hvg"></a>



"""

def hvg(y):  # на вход массив значений
    # #на выходе отсортированый массив(target source)
    source_target = []
    for i in tqdm(range(len(y) - 1)):
        source_target.append([i + 1, i + 2])
        
        for j in range(i + 2, len(y)):
            flg = False
            for k in range(i + 1, j):
                if y[i] > y[k] and y[j] > y[k]:
                    flg = True
                else:
                    flg = False
                    break

            if flg:
                source_target.append([i + 1, j + 1])
    return source_target

"""#### Скользящее окно для nvg<a name="snvg"></a>"""

def snvg(y, k):
    n = len(y)
    #k = 100  
    source_target = nvg(y[:k])

    for i in tqdm(range(k, n)):
        source_target.append([i, i + 1])
        for j in range(i - k, i - 1):
            flg = False
            for z in range(j + 1, i):
                if y[z] < y[j] + ((y[i] - y[j]) * ((j - z) / (j - i))):
                    flg = True
                else:
                    flg = False
                    break

            if flg:
                source_target.append([j + 1, i + 1])
                
    return source_target

"""#### Скользящее окно для hvg<a name="shvg"></a>"""

def shvg(y, k):
    n = len(y)
    #k = 100  
    source_target = hvg(y[:k])

    for i in tqdm(range(k, n)):
        source_target.append([i, i + 1])
        for j in range(i - k, i - 1):
            flg = False
            for z in range(j + 1, i):
                if y[i] > y[z] and y[j] > y[z]:
                    flg = True
                else:
                    flg = False
                    break

            if flg:
                source_target.append([j + 1, i + 1])
                
    return source_target

"""### 3. Функция для работы с пользователем<a name="user"></a>"""

def start(x, alg, razmer=0):
    #audio_data = input("Введите путь до аудио файла: ")
    #sr = int(input("Введите частоту дискретизации:"))
    #x, sr = librosa.load(audio_data, sr)
    #alg = input("Введите алгоритм:")
    if alg == 'nvg':
        result = pd.DataFrame(nvg(x), columns=['Source', 'Target'])
    elif alg == 'hvg':
        result = pd.DataFrame(hvg(x), columns=['Source', 'Target'])
    elif alg == 'snvg':
        result = pd.DataFrame(snvg(x,razmer), columns=['Source', 'Target'])
    elif alg == 'shvg':
        result = pd.DataFrame(shvg(x,razmer), columns=['Source', 'Target'])
        
    print('задача выполнена')
    result.to_csv('/content/result.csv', index=False)

    
    files.download('/content/result.csv')