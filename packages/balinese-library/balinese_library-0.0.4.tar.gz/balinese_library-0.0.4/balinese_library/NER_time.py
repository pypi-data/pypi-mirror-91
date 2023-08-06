import glob
import os
import codecs
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import re

stop = ['sane', 'ipun', 'ane']
day = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu', 'radite','redite','soma', 'anggara', 'buda', 'respati', 'wraspati', 'wrehaspati', 'sukra', 'saniscara']
month = ['januari', 'februari', 'maret', 'april', 'mei', 'juni','juli', 'agustus', 'september', 'oktober', 'november', 'desember']
date_prefix = ['tahun', 'abad','sasih','bulan','pinanggal', 'dugas', 'dina', 'rahina', 'warsa','duk', 'ngawit', 'periode', 'tanggal', 'sue', 'suene', 'suennyane']
date_sufix = ['lintang', 'mangkin', 'iriki','kaon', 'riin', 'liwat', 'inuni', 'rauh']
date_range = ['nyantos','kantos']
numStr = ['sik','dua', 'a', 'i','kalih', 'tigang', 'telung', 'telu', 'papat','patpat', 'lima', 'nem','nenem', 'pitu', 'kutus', 'sia', 'dasa', 'solas', 'limolas']
duration = ['detik', 'jam', 'dina', 'minggu','menit', 'tiban', 'warsa', 'sasih', 'lemeng']
durationStr = ['abulan', 'telun', 'atiban', 'awai']
notDatePrefix = ['matuuh', 'mayusa', 'no', 'nomer', 'pergub', 'perda']


# s
def preprocessing(text):
    text = text.replace('é', 'e')
    text = text.lower()
    text = nltk.tokenize.word_tokenize(text)
    symbols = "',!\"#$%&()*+.:;<=>?@[\]^_`{|}~\n"
    for i in symbols:
        text = np.char.replace(text, i, '')
        kalimatt = []
    rKalimat = []
    for i in text:
        if i in stop:
            continue
        else:
            rKalimat.append(i)
    text = rKalimat
    for elem in text:
        if elem:
            kalimatt.append(elem)
    # print(kalimatt)
    return kalimatt

def rule(txtPrep, pWaktu):
    for index, i in enumerate(txtPrep):
        # format tanggal Hari 28/08/2019 atau Hari 28-9-2019 atau tgl tok
        if '/' in i or '-' in i:
            m = re. match(
                '(\d{1}|\d{2})[/-](\d{1}|\d{2})[/-](\d{4})', txtPrep[index])
            n = re. match('(\d{1}|\d{2})[/](\d{1}|\d{2})', txtPrep[index])
            # print(m)
            if m or n:
                x = txtPrep[index-1]
                if (x in day):
                    a = x + ' ' + i
                    pWaktu.append(a)
                if txtPrep[index-2] in day:
                    a = x + ' ' + txtPrep[index-2]
                    pWaktu.append(a)
                if x not in day and txtPrep[index-2] not in day and x not in notDatePrefix and txtPrep[index-2] not in notDatePrefix :
                    if m:
                        pWaktu.append(m)
                    if n: 
                        pWaktu.append(n)
            else:
                continue

        # format rentang dengan kata hubung ex: nyantos
        if i in date_range:
            x = txtPrep[index-1]
            y = txtPrep[index+1]
            z = txtPrep[index+2]
            # ex: 60-90 tiban
            if (x.isnumeric() == True and y.isnumeric() == True) and z in duration:
                a = x + '-' + y + z
                pWaktu.append(a)
            # ex: 2014-2019
            if (x.isnumeric() == True and y.isnumeric() == True) and z not in duration and z not in month:
                a = x + '-' + y
                pWaktu.append(a)
            # ex: 1 nyantos 12 februari
            if (x.isnumeric() == True and y.isnumeric() == True) and z in month:
                if txtPrep[index+3].isnumeric()==True:
                    a = x + '-' + y + ' ' + z + ' '+txtPrep[index+3]
                    pWaktu.append(a)
                else:
                    a = x + '-' + y + ' ' + z 
                    pWaktu.append(a)
            
            # ex: 6 sasih
            if z in duration:
                a = y + ' ' + z
                pWaktu.append(a)

        # atiban ane liwat
        if i in durationStr:
            if txtPrep[index-1] not in date_prefix or txtPrep[index-1] not in range:
                if txtPrep[index+1] in date_sufix:
                    a = i + ' ' + txtPrep[index+1]
                    pWaktu.append(a)
                if txtPrep[index+2] in date_sufix:
                    a = i + ' ' + txtPrep[index+2]
                    pWaktu.append(a)
                if txtPrep[index+1] not in date_sufix and txtPrep[index+2] not in date_sufix:
                    pWaktu.append(i)
        # limolas menit, mayusa 40 tahun tidak akan diambil
        if i in numStr or i.isnumeric() == True:
            if 'no' in txtPrep[index-1] or 'nomer' in txtPrep[index-1] or 'nomor' in txtPrep[index-1] or txtPrep[index-1] in notDatePrefix :
                continue
            if txtPrep[index-1] not in date_prefix and txtPrep[index-1] not in day and txtPrep[index-1] not in date_range:
                try:
                    if txtPrep[index+1] in month:
                        if txtPrep[index+2].isnumeric() == True:
                            if txtPrep[index+3] in date_sufix:
                                a = i + ' ' + txtPrep[index +1] + ' ' + txtPrep[index+2]+' '+txtPrep[index+3]
                                pWaktu.append(a)
                            else:
                                a = i + ' ' + txtPrep[index +1] + ' ' + txtPrep[index+2]
                                pWaktu.append(a)
                        if txtPrep[index+2].isnumeric() == False:
                            if txtPrep[index+2] in date_sufix:
                                a = i + ' ' + txtPrep[index +1] + ' ' + txtPrep[index+2]
                                pWaktu.append(a)
                            else:
                                a = i + ' ' + txtPrep[index+1]
                                pWaktu.append(a)

                    if txtPrep[index+1] in duration:
                        if txtPrep[index+2] in date_sufix:
                            a = i + ' ' + txtPrep[index+1] + ' ' + txtPrep[index+2]
                            pWaktu.append(a)
                        if txtPrep[index+3] in date_sufix:
                            a = i + ' ' + txtPrep[index+1] + ' ' + txtPrep[index+3]
                            pWaktu.append(a)
                        if txtPrep[index+2] not in date_sufix and txtPrep[index+3] not in date_sufix:
                            a = i + ' ' + txtPrep[index+1]
                            pWaktu.append(a)
                except:
                    continue
        # format warsa 1990, kalau pergub no xx warsa atau tahun xx ga di detect
        if i in date_prefix:
            z = txtPrep[index-2]
            if 'no' in z or 'nomer' in z or 'pergub' in z or 'perda' in z:
                continue
            else:
                try:
                    x = txtPrep[index+1]
                    y = txtPrep[index+2]
                    z = txtPrep[index+3]
                    j = txtPrep[index+4]
                    if x.isnumeric() == True or x in numStr:
                        # ex: duk 1000 warsa sane sampun lintang, 1998 sane lintang, 1998
                        if y in duration:
                            if z in date_sufix:
                                a = x + ' ' + y + ' ' + z
                                pWaktu.append(a)
                            if j in date_sufix:
                                a = x + ' ' + y + ' ' + j
                                pWaktu.append(a)
                            if z not in date_sufix and j not in date_sufix:
                                a = x + ' ' + y
                                pWaktu.append(a)
            
                        if y not in duration and y not in month and y not in date_range:
                            if y in date_sufix:
                                a = x + ' ' + y
                                pWaktu.append(a)
                            if z in date_sufix:
                                a = x + ' ' + z
                                pWaktu.append(a)
                            if j in date_sufix:
                                a = x + ' ' + j
                                pWaktu.append(a)
                            if y not in duration and y not in date_sufix and z not in date_sufix and j not in date_sufix and '-' not in y:
                                pWaktu.append(x)
                    # warsane mangkin
                    if (txtPrep[index-1].isnumeric() == True or txtPrep[index-1] in numStr):
                        continue
                    if (txtPrep[index-1].isnumeric() == False or txtPrep[index-1] not in numStr) and x.isnumeric() == False:
                        if x in date_sufix:
                            a = i + ' ' + x
                            pWaktu.append(a)
                        if y in date_sufix:
                            a = i + ' ' + y
                            pWaktu.append(a)
                    if y.isnumeric() == True or y in numStr:
                        if z in duration:
                            a = y + ' ' + z
                            pWaktu.append(a)
                    if x in day and y.isnumeric() == False and z not in month and '/' not in y:
                        pWaktu.append(x)
                    # ex: duk 1000 warsa sane sampun lintang, biar duk sama warsa ga tabrakan
                    if txtPrep[index-2] in date_prefix or txtPrep[index-1] in date_prefix:
                        continue
                    # 80-an
                    if '-an' in x or 'ke-' in x:
                        if y in date_range:
                            a = x + '-' + z
                            pWaktu.append(a)
                        else:
                            a = i + ' ' + x
                            pWaktu.append(a)
                    # ex: periode 2019-2020
                    if '-' in x:
                        removed = x.replace('-', '')
                        rlen = len(removed)
                        if rlen == 8:
                            pWaktu.append(x)
                    if x.isnumeric() == True:
                        rlen = len(x)
                        if rlen == 4:
                            if '-' in y and z.isnumeric() == True:
                                a = x + y + z
                                pWaktu.append(a)
                except:
                    continue
                m = 0
                words = []
                while m < 7:
                    words.append(txtPrep[index])
                    m = m + 1
                    index = index + 1
                # format hari 10 januari 2019 atau 10 januari 2019 atau 10 januari
                for index, i in enumerate(words):
                    try:
                        if i in month:
                            x = words[index-1]
                            y = words[index+1]
                            z = words[index-2]
                            j = words[index+2]
                            k = words[index+3]
                            if z in day and x.isnumeric() == True and y.isnumeric() == True:
                                a = z + ' ' + x + ' ' + i + ' ' + y
                                pWaktu.append(a)
                            if z not in day and x.isnumeric() == True and y.isnumeric() == True:
                                a = x + ' ' + i + ' ' + y
                                pWaktu.append(a)
                            if x.isnumeric() == True and y.isnumeric() == False and y not in date_range:
                                a = x + ' ' + i
                                pWaktu.append(a)
                            if x.isnumeric() == False and y.isnumeric() == True:
                                a = i + ' ' + y
                                pWaktu.append(a)
                            # 17-18 mei
                            if '-' in x:
                                if y.isnumeric() == True and j in date_sufix:
                                    a = x + ' ' + i + ' ' + y + ' ' + j
                                    pWaktu.append(a)
                                if y.isnumeric() == False and j in date_sufix:
                                    a = x + ' ' + i + ' ' + y + ' ' + j
                                    pWaktu.append(a)
                                if y.isnumeric() == True and k in date_sufix:
                                    a = x + ' ' + i + ' ' + y + ' ' + k
                                    pWaktu.append(a)
                                if y.isnumeric() == False and k in date_sufix:
                                    a = x + ' ' + i + ' ' + k
                                    pWaktu.append(a)
                                if y.isnumeric() == True and j not in date_sufix and k not in date_sufix:
                                    a = x + ' ' + i + ' ' + y
                                    pWaktu.append(a)
                                if y.isnumeric() == False and j not in date_sufix and k not in date_sufix:
                                    a = x + ' ' + i + ' ' + y
                                    pWaktu.append(a)
                            if y in date_range and k in month:
                                if x.isnumeric() == True:
                                    if words[index+4].isnumeric() == True:
                                        a = x + ' ' + i + '-' + j + ' ' + k + ' '+ words[index+4]
                                        pWaktu.append(a)
                                    else:
                                        a = x + ' ' + i + '-' + j + ' ' + k
                                        pWaktu.append(a)
                            if words[index-2] in date_range and words[index-3] in month:
                                continue
                    except:
                        continue
        # yg tidak diawalin prefix
        if i in day and txtPrep[index-1] not in date_prefix:
            if '/' in txtPrep[index+1] or '-' in txtPrep[index+1]:
                continue
            if txtPrep[index+2] in month:
                a = i + ' ' + txtPrep[index+1] + ' ' + txtPrep[index+2] + ' ' + txtPrep[index+3]
                pWaktu.append(a)
            if txtPrep[index-1] not in date_prefix and txtPrep[index+2] not in month:
                pWaktu.append(i)
    return pWaktu
    
def ner_time(sentences):
    string = sentences
    prep = preprocessing(string)
    pWaktu = []
    pWaktu = rule(prep, pWaktu)
    time = ', '.join(map(str, pWaktu))
    time = "Time : " + time 
    return time