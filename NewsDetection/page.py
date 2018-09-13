# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 09:48:09
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-13 23:56:16

from django.shortcuts import render

from dict.models import News
import codecs
import json

def show(request):
    news_id = request.GET.get('p','')
    if news_id.isdigit() and news_id != '':
        try:
            data_file = codecs.open('data/html_'+str(news_id),'r','utf-8')
            news = json.loads(data_file.read())
            data_file.close()
            print('news_id', news)
            context           = {}
            context['title']  = news['title']
            context['time']   = news['time']
            context['source'] = news['source']
            context['text']   = news['text'].splitlines()
            return render(request, 'page.html', context)
        except:
            return render("404.html", {})
    else:
        return render("404.html", {})

