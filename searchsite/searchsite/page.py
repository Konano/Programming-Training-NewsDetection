# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 09:48:09
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-13 12:21:48

file_size = 1000

from django.shortcuts import render
import codecs
import json

def show(request):
    news_id = request.GET.get('p','')
    if news_id.isdigit() and news_id != '':
        try:
            news_id = int(news_id)
            file_id = (news_id-1) // file_size + 1
            news_id = (news_id-1) % file_size
            print('file_id:', file_id, 'news_id:', news_id)
            data_file = codecs.open('../data/data_'+str(file_id),'r','utf-8')
            data = json.loads(data_file.read())
            data_file.close()
            context           = {}
            context['title']  = data[news_id]['title']
            context['time']   = data[news_id]['time']
            context['source'] = data[news_id]['source']
            context['text']   = data[news_id]['text'].splitlines()
            return render(request, 'page.html', context)
        except:
            return render("404.html", {})
    else:
        return render("404.html", {})

