# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 22:13:47
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-14 09:54:40

page_show = 20

from django.shortcuts import render
import jieba
import re
import time
import codecs
import json
from urllib import parse

from dict.models import Word, News, Include

def highlight(text, word_list):
    for word in word_list:
        text = ('<em>'+word+'</em>').join(text.split(word))
    return re.compile(r'[\s]').sub('',text)

def search(search_word, search_word_list):
    collect = []
    for word in search_word_list:
        try:
            collect.extend(list(map(lambda x : x.label, Word.objects.get(name=word).news.all())))
        except:
            collect.extend([])

    tmp = list(set(collect))
    count = list(map(lambda x : collect.count(x), tmp))
    result = list(map(lambda x:x[0], sorted(list(map(lambda x,y:(x,y), tmp, count)), key=lambda x:x[1], reverse=True)))

    file = codecs.open('log/'+parse.quote_plus(search_word),'w','utf-8')
    file.write(json.dumps(result))
    file.close()
    print('search completed')
    return result

def page(request, search_word, page_num):
    start = time.time()
    print('search_word', search_word)
    search_word_list = jieba.lcut(search_word)
    print('search_word_list', search_word_list)
    try:
        _file = codecs.open('log/'+parse.quote_plus(search_word),'r','utf-8')
        result = json.loads(_file.read())
        _file.close()
    except:
        result = search(search_word, search_word_list)

    page_max = max(1, (len(result)-1) // page_show + 1)
    if page_num > page_max:
        page_num = page_max
    if page_num < 1:
        page_num = 1
    news_start = (page_num-1) * page_show
    news_end   = min(len(result), page_num * page_show)

    context                      = {}
    context['search_text']       = search_word
    context['search_text_quote'] = parse.quote_plus(search_word)
    context['result_total']      = len(result)
    context['cost_time']         = time.time() - start
    context['result']            = []
    context['page_pre']          = page_num - 1 if page_num != 1 else 0
    context['page_next']         = page_num + 1 if page_num != page_max else 0
    context['page_now']          = page_num
    context['page']              = range(max(1, page_num-5), min(page_max+1, page_num+5))

    for news_id in result[news_start:news_end]:
        data_file = codecs.open('data/html_'+str(news_id),'r','utf-8')
        news = json.loads(data_file.read())
        data_file.close()
        context['result'].append({ \
            'id'      : str(news_id), \
            'title'   : news['title'], \
            'time'    : news['time'][:10], \
            'preview' : highlight(news['text'][:250],search_word_list)})

    return render(request, 'search.html', context)

def index(request, page_num):
    start = time.time()
    news_total = News.objects.count()
    page_max = max(1, (news_total-1) // page_show + 1)
    if page_num > page_max:
        page_num = page_max
    if page_num < 1:
        page_num = 1
    context                 = {}
    context['result_total'] = news_total
    context['cost_time']    = time.time() - start
    context['result']       = []
    context['page_pre']     = page_num - 1 if page_num != 1 else 0
    context['page_next']    = page_num + 1 if page_num != page_max else 0
    context['page_now']     = page_num
    context['page']         = range(max(1, page_num-5), min(page_max+1, page_num+5))
    news_start = (page_num-1) * page_show + 1
    news_end   = min(news_total, page_num * page_show)
    for news_id in range(news_start, news_end+1):
        data_file = codecs.open('data/html_'+str(news_id),'r','utf-8')
        news = json.loads(data_file.read())
        data_file.close()
        context['result'].append({ \
            'id'      : str(news_id), \
            'title'   : news['title'], \
            'time'    : news['time'][:10], \
            'preview' : highlight(news['text'][:250],[])})

    return render(request, 'search_index.html', context)

def show(request):
    if 'w' in request.GET:
        search_word = parse.unquote_plus(request.GET['w'])
        page_num = request.GET.get('p','')
        if page_num.isdigit() or page_num == '':
            if page_num == '':
                page_num = 1
            else:
                page_num = int(page_num)
            return page(request, search_word, page_num)
        else:
            return render("404.html", {})
    else:
        page_num = request.GET.get('p','')
        if page_num.isdigit() or page_num == '':
            if page_num == '':
                page_num = 1
            else:
                page_num = int(page_num)
            return index(request, page_num)
        else:
            return render("404.html", {})