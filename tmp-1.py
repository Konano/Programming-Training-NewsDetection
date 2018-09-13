# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 22:54:14
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-13 18:18:21

import os
import django

os.environ.update({"DJANGO_SETTINGS_MODULE": "NewsDetection.settings"})
# os.environ.setdefault('DJANGO_SETTING_MODULE', 'NewsDetection.settings')
django.setup()

from news.models import News
# from dict.models import Dict
import json
import codecs
import jieba
import re

data_file_start = 2
data_file_end = 21
file_size = 1000

# d = {}

# def remove_punctuation(line):
#     rule = re.compile(r'[^\0\u4e00-\u9fa5]')
#     line = rule.sub('',line)
#     return line.lower()

# def save_d():
#     global d
#     # print(d)
#     d_file = codecs.open('dict.txt','w','utf-8')
#     d_file.write(json.dumps(d))
#     d_file.close()
#     print('Save dict! Dict size:', len(d))

if __name__ == '__main__':
    waitforadd = []
    news_id = (data_file_start-1) * file_size
    for file_id in range(data_file_start, data_file_end):
        print('Start split file', file_id)
        data_file = codecs.open('data/data_'+str(file_id),'r','utf-8')
        data = json.loads(data_file.read())
        data_file.close()
        for news in data:
            news_id += 1
            waitforadd.append(News( \
                label  = news_id, \
                title  = news['title'], \
                source = news['source'], \
                time   = news['time'], \
                text   = news['text']))
    News.objects.bulk_create(waitforadd)
        # file_d = []
        # for news in data:
        #     news_id += 1
        #     new_d = {}
        #     for word in jieba.lcut_for_search(remove_punctuation(news['title'])):
        #         if word in new_d:
        #             new_d[word] += 10
        #         else:
        #             new_d[word] = 10
        #         if word in d:
        #             if d[word][-1] != news_id:
        #                 d[word].append(news_id)
        #         else:
        #             d[word] = [news_id]
        #     for word in jieba.lcut_for_search(remove_punctuation(news['text'])):
        #         if word in new_d:
        #             new_d[word] += 1
        #         else:
        #             new_d[word] = 1
        #         if word in d:
        #             if d[word][-1] != news_id:
        #                 d[word].append(news_id)
        #         else:
        #             d[word] = [news_id]
        #     file_d.append(new_d)
        #     if news_id % 100 == 0:
        #         save_d()
        # split_file = codecs.open('split/data_'+str(file_id),'w','utf-8')
        # split_file.write(json.dumps(file_d))
        # split_file.close()
    # print(d)
