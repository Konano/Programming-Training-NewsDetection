# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 22:54:14
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-12 00:25:38

import json
import codecs
import jieba
import re

data_file_start = 1
data_file_end = 18
file_size = 1000

d = {}

def remove_punctuation(line):
    rule = re.compile(r'[^\0\u4e00-\u9fa5]')
    line = rule.sub('',line)
    return line.lower()

def save_d():
    global d
    # print(d)
    d_file = codecs.open('dict.txt','w','utf-8')
    d_file.write(json.dumps(d))
    d_file.close()
    print('Save dict! Dict size:', len(d))

if __name__ == '__main__':
    d_file = codecs.open('dict.txt','r','utf-8')
    d = json.loads(d_file.read())
    d_file.close()
    # print(len(d))
    news_id = (data_file_start-1) * file_size
    for file_id in range(data_file_start, data_file_end):
        print('Start split file', file_id)
        data_file = codecs.open('data/date_'+str(file_id),'r','utf-8')
        data = json.loads(data_file.read())
        data_file.close()
        file_d = []
        for news in data:
            news_id += 1
            seg_list = jieba.lcut_for_search(remove_punctuation(news['title']))
            seg_list.extend(jieba.lcut_for_search(remove_punctuation(news['text'])))
            # print(", ".join(seg_list))
            new_d = {}
            for word in seg_list:
                if word in new_d:
                    new_d[word] += 1
                else:
                    new_d[word] = 1
                if word in d:
                    if d[word][-1] != news_id:
                        d[word].append(news_id)
                else:
                    d[word] = [news_id]
            file_d.append(new_d)
            if news_id % 100 == 0:
                save_d()
        split_file = codecs.open('split/date_'+str(file_id),'w','utf-8')
        split_file.write(json.dumps(file_d))
        split_file.close()
    # print(d)

