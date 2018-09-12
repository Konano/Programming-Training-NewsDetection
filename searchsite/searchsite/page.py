# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 09:48:09
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-12 15:55:50

file_size = 1000

from django.shortcuts import render
import codecs
import json

def show(request, news_id):
    news_id = int(news_id)
    file_id = (news_id-1) // file_size + 1
    news_id = (news_id-1) % file_size
    print('file_id:', file_id, 'news_id:', news_id)
    data_file = codecs.open('data/data_'+str(file_id),'r','utf-8')
    data = json.loads(data_file.read())
    data_file.close()
    context           = {}
    context['title']  = data[news_id]['title']
    context['time']   = data[news_id]['time']
    context['source'] = data[news_id]['source']
    context['text_list']   = data[news_id]['text'].splitlines()
    return render(request, 'page.html', context)
