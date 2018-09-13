# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-14 01:28:54
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-14 01:57:21

import codecs
import json
import jieba
import jieba.analyse

news_start = 1
news_end = 10

def relate(a, b):
    value = 0
    tag = list(set(map(lambda x:x[0], b)) & set(map(lambda x:x[0], a)))
    # print(a, b, tag)
    for word in tag:
        value += list(filter(lambda x:x[0]==word, a))[0][1] * list(filter(lambda x:x[0]==word, b))[0][1]
    # print(value)
    return value

if __name__ == '__main__':
    tags = {}
    re = {}
    for news_id in range(news_start, news_end+1):
        if news_id % 100:
            print('Now', news_id)
        data_file = codecs.open('data/html_'+str(news_id),'r','utf-8')
        news = json.loads(data_file.read())
        data_file.close()
        tags[news_id] = jieba.analyse.extract_tags(news['text'], withWeight=True)
        re[news_id] = []

    print('Read OK!')
    for news_id in range(news_start, news_end+1):
        print('Now', news_id)
        for _news_id in range(news_id+1, news_end+1):
            value = relate(tags[news_id], tags[_news_id])
            re[news_id].append((_news_id, value))
            re[_news_id].append((news_id, value))

        data_file = codecs.open('data/html_'+str(news_id),'r','utf-8')
        news = json.loads(data_file.read())
        data_file.close()
        news['relate'] = list(map(lambda x:x[0], sorted(re[news_id], key=lambda x:x[1], reverse=True)[:3]))
        data_file = codecs.open('data/html_'+str(news_id),'w','utf-8')
        data_file.write(json.dumps(news))
        data_file.close()
