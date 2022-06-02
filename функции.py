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

### 1. Загрузка библиотек<a name="load_bibl"></a>
"""

pip install pydub

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

import math as m
from pydub import AudioSegment

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

def start(name_file ,x, alg, razmer=0):
    name_file = name_file.split('.')[0]
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
    result.to_csv('/content/res_'+name_file+'_'+alg+'.csv', index=False)

    
    files.download('/content/res_'+name_file+'_'+alg+'.csv')

def start_music(name_file1, sr, alg, razmer=0):
    name_file = name_file1.split('.')[0]
    audio_data = '/content/'+ name_file1
    x, sr = librosa.load(audio_data, sr)

    if alg == 'nvg':
        result = pd.DataFrame(nvg(x), columns=['Source', 'Target'])
    elif alg == 'hvg':
        result = pd.DataFrame(hvg(x), columns=['Source', 'Target'])
    elif alg == 'snvg':
        result = pd.DataFrame(snvg(x,razmer), columns=['Source', 'Target'])
    elif alg == 'shvg':
        result = pd.DataFrame(shvg(x,razmer), columns=['Source', 'Target'])
        
    print('задача выполнена')
    result.to_csv('/content/res_'+name_file+'_'+alg+'.csv', index=False)

    
    files.download('/content/res_'+name_file+'_'+alg+'.csv')

def razdel(otrz, razr, name_file, sr, alg, razmer=0):
  if razr == 'wav':
    sound = AudioSegment.from_wav(audio_data)
  elif  razr == 'mp3':
    sound = AudioSegment.from_mp3(audio_data)

    
  audio_data = '/content/' + name_file
 
  s = m.floor(len(sound)/otrz)
  k = 0
  for i in range(otrz,len(sound),otrz):
    k += 1
    new_name = name_file.split('.')[0] + '_' + str(k)+ '.'+razr
    sound[i-otrz: i].export('/content/'+ new_name, format=razr)
    start_music(new_name, sr, alg, razmer)
    if k == s:
      k += 1
      new_name = name_file.split('.')[0] + '_' + str(k)+ '.'+razr
      sound[i:].export('/content/'+ new_name, format=razr)
      start_music(new_name, sr, alg, razmer)
      break