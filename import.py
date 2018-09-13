# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 22:54:14
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-13 23:48:44

import os
# os.environ.setdefault('DJANGO_SETTING_MODULE', 'NewsDetection.settings')
os.environ.update({"DJANGO_SETTINGS_MODULE": "NewsDetection.settings"})

import django
django.setup()
from dict.models import Word, News, Include

import json
import codecs
import jieba
import re
import time

data_file_start = 1
data_file_end = 1
file_size = 1000

def remove_punctuation(line):
    rule = re.compile(r'[^\0\u4e00-\u9fa5]')
    line = rule.sub('',line)
    return line.lower()

def clear():
    Word.objects.all().delete()
    News.objects.all().delete()
    # exit()

if __name__ == '__main__':
    if data_file_start == 1:
        clear()
    d = {}
    waitforadd = []
    news_id = (data_file_start-1) * file_size
    for file_id in range(data_file_start, data_file_end+1):
        print('Start import file', file_id)
        data_file = codecs.open('data/data_'+str(file_id),'r','utf-8')
        data = json.loads(data_file.read())
        data_file.close()

        for news in data:
            news_id += 1
            if news_id > 10:
                break
            waitforadd.append(News(label=news_id))

            data_file = codecs.open('data/html_'+str(news_id),'w','utf-8')
            data_file.write(json.dumps({ \
                'label'  : news_id, \
                'title'  : news['title'], \
                'source' : news['source'], \
                'time'   : news['time'], \
                'text'   : news['text']}))
            data_file.close()

            count = jieba.lcut_for_search(remove_punctuation(news['title'])) + \
                    jieba.lcut_for_search(remove_punctuation(news['text']))

            for word in list(set(count)):
                if (word in d) == False:
                    d[word] = []
                d[word].append(news_id)

    News.objects.bulk_create(waitforadd)
    news_ls = [None]*(news_id+1)
    for item in waitforadd:
        news_ls[item.label] = News.objects.get(label=item.label)

    waitforadd = []
    total = 0
    all_total = len(d.keys())
    for word in d.keys():
        total += 1
        if total % 50 == 0:
            print(total, all_total, str(total/all_total*100)+'%')
        tmp = Word.objects.get_or_create(name=word)[0]
        for item in d[word]:
            waitforadd.append(Include(word=tmp, news=news_ls[item]))
    Include.objects.bulk_create(waitforadd)
