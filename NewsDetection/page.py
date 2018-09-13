# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 09:48:09
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-13 17:11:12

from django.shortcuts import render

from news.models import News

def show(request):
    news_id = request.GET.get('p','')
    if news_id.isdigit() and news_id != '':
        try:
            news = News.objects.get(label=int(news_id))
            print('news_id', news)
            context           = {}
            context['title']  = news.title
            context['time']   = news.time
            context['source'] = news.source
            context['text']   = news.text.splitlines()
            return render(request, 'page.html', context)
        except:
            return render("404.html", {})
    else:
        return render("404.html", {})

