# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 09:48:09
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-14 11:04:29

from django.shortcuts import render

from dict.models import News
import codecs
import json
import re

def preview(text):
    text = re.compile(r'[\s]').sub('',text)
    if '。' in text:
        return text[:text.index('。')+1]
    else:
        return text[:min(len(text),50)]

def show(request):
    news_id = request.GET.get('p','')
    if news_id.isdigit() and news_id != '':
        try:
            data_file = codecs.open('data/html_'+str(news_id),'r','utf-8')
            news = json.loads(data_file.read())
            data_file.close()
            print('news_id', news['title'])
            context           = {}
            context['title']  = news['title']
            context['time']   = news['time']
            context['source'] = news['source']
            context['text']   = news['text'].splitlines()
            context['relate'] = []
            if 'relate' in news:
                for relate_id in news['relate']:
                    data_file = codecs.open('data/html_'+str(relate_id),'r','utf-8')
                    relate_news = json.loads(data_file.read())
                    data_file.close()
                    context['relate'].append({'id':relate_id, \
                                              'title':relate_news['title'], \
                                              'time':relate_news['time'], \
                                              'preview':preview(relate_news['text'])})

            return render(request, 'page.html', context)
        except:
            return render("404.html", {})
    else:
        return render("404.html", {})

