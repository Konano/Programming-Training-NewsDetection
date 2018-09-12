# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 22:13:47
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-13 02:38:32

file_size = 1000
page_show = 20

from django.shortcuts import render
import codecs
import json
import jieba
import re
import time
from urllib import parse

file_id = 0
data = {}
split = {}

def openfile(id):
    # print('open file', id)
    global file_id, data, split
    file_id = id
    file = codecs.open('../data/data_'+str(id),'r','utf-8')
    data = json.loads(file.read())
    file.close()
    file = codecs.open('../split/data_'+str(id),'r','utf-8')
    split = json.loads(file.read())
    file.close()

def count(news_id, word):
    _file_id = (news_id-1) // file_size + 1
    news_id = (news_id-1) % file_size
    if file_id != _file_id:
        openfile(_file_id)
    if word in split[news_id]:
        return split[news_id][word]
    return 0

def get_time(news_id):
    _file_id = (news_id-1) // file_size + 1
    news_id = (news_id-1) % file_size
    if file_id != _file_id:
        openfile(_file_id)
    return data[news_id]['time']

def get_title(news_id):
    _file_id = (news_id-1) // file_size + 1
    news_id = (news_id-1) % file_size
    if file_id != _file_id:
        openfile(_file_id)
    return data[news_id]['title']

def get_preview(news_id):
    _file_id = (news_id-1) // file_size + 1
    news_id = (news_id-1) % file_size
    if file_id != _file_id:
        openfile(_file_id)
    return data[news_id]['text'][:250]

def highlight(text, word_list):
    for word in word_list:
        text = ('<em>'+word+'</em>').join(text.split(word))
    return re.compile(r'[\s]').sub('',text)

def search(search_word):
    print('search_word', search_word)
    search_word_list = jieba.lcut(search_word)
    print('search_word_list', search_word_list)
    dic_file = codecs.open('../dict.txt','r','utf-8')
    dic = json.loads(dic_file.read())
    dic_file.close()
    print('read dict.txt completed, start to count')
    _result = {}
    _dic = []
    for word in search_word_list:
        if word in dic:
            _dic = list(set(_dic + dic[word]))
        else:
            search_word_list.remove(word)
    print('search_word_list', search_word_list)
    _dic.sort()
    for news_id in _dic:
        for word in search_word_list:
            if news_id in dic[word]:
                if news_id in _result:
                    _result[news_id]['times']  += count(news_id, word)
                else:
                    _result[news_id]            = {}
                    _result[news_id]['times']   = count(news_id, word)
                    _result[news_id]['id']      = str(news_id)
                    _result[news_id]['title']   = get_title(news_id)
                    _result[news_id]['time']    = get_time(news_id)[:10]
                    _result[news_id]['preview'] = highlight(get_preview(news_id), search_word_list)

    print('count completed, start to export')
    result = []
    for item in sorted(_result.items(), key=lambda item:item[1]['times'], reverse=True):
        result.append(item[1])
    # print(result)
    file = codecs.open('log/'+parse.quote_plus(search_word),'w','utf-8')
    file.write(json.dumps(result))
    file.close()
    print('export completed')

    return result

def page(request, search_word, page_num):
    start = time.time()
    try:
        file = codecs.open('log/'+parse.quote_plus(search_word),'r','utf-8')
        result = json.loads(file.read())
        file.close()
    except:
        result = search(search_word)
    page_max = max(1, (len(result)-1) // page_show + 1)
    if page_num > page_max:
        page_num = page_max
    if page_num < 1:
        page_num = 1
    news_start = (page_num-1) * page_show
    news_end   = min(len(result), page_num * page_show)

    # print(page_num, page_max, news_start, news_end)

    context                      = {}
    context['search_text']       = search_word
    context['search_text_quote'] = parse.quote_plus(search_word)
    context['result_total']      = len(result)
    context['cost_time']         = time.time() - start
    context['result']            = result[news_start:news_end]
    context['page_pre']          = page_num - 1 if page_num != 1 else 0
    context['page_next']         = page_num + 1 if page_num != page_max else 0
    context['page_now']          = page_num
    context['page']              = range(max(1, page_num-5), min(page_max+1, page_num+5))
    return render(request, 'search.html', context)

def show(request):
    search_word = parse.unquote_plus(request.GET.get('w',''))
    page_num = request.GET.get('p','')
    if search_word.isspace() == False:
        if page_num.isdigit() or page_num == '':
            if page_num == '':
                page_num = 1
            else:
                page_num = int(page_num)
            return page(request, search_word, page_num)
        else:
            return render("404.html", {})
    else:
        return index(request)