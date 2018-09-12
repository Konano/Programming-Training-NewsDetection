# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 00:47:45
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-13 03:21:16

import urllib.request
import re
import time
import codecs
from bs4 import BeautifulSoup
import json
import random

maxlen = 1000
total = 0
file_size = 1000
file_id = 0

catched_url = {}
catched_title = {}

def getURLContent(url):
    # print ("getURLContent: ", url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url = url, headers = headers)
    content = urllib.request.urlopen(req, timeout = 10).read()
    return content.decode('utf-8','ignore')

def extract(content):
    news = {}
    soup = BeautifulSoup(content, 'lxml')
    news['title'] = soup.find('div', class_='h-title').get_text().strip()
    news['time'] = soup.find('span', class_='h-time').get_text().strip()
    try:
        news['source'] = soup.find(id='source').get_text().strip()
    except:
        news['source'] = soup.find('span', class_='aticle-src').get_text().strip()
    news['text'] = ''
    for text in soup.find(id='p-detail').find_all('p'):
        news['text'] += text.get_text().strip('</p>') + '\n'

    print(news['title'])
    return news

def nextPage(content):
    p = re.compile(r'http://www.xinhuanet.com/[\/\-\w]+.htm')
    return p.findall(content)

if __name__ == '__main__':

    # URL = []
    URL = ['http://www.xinhuanet.com/index.htm']
    # URL = ['http://www.xinhuanet.com/2018-05/22/c_1122870950.htm']

    # catched_file = codecs.open('catched_url.txt','r','utf-8')
    # catched_log = catched_file.readlines()
    # catched_file.close()
    # for i in catched_log:
    #     catched_url[i] = True

    # catched_file = codecs.open('catched_title.txt','r','utf-8')
    # catched_log = catched_file.readlines()
    # catched_file.close()
    # for i in catched_log:
    #     catched_title[i] = True

    # while len(URL) < maxlen:
    #     try:
    #         content = getURLContent(random.choice(catched_log))
    #     except:
    #         nothing = True
    #     else:
    #         for i in nextPage(content):
    #             if (i in catched_url) == False and i.find('photo') == -1 and i.find('video') == -1:
    #                 URL.append(i)
    #                 catched_url[i] = True

    catched_url[URL[0]] = True

    catched_url_file = codecs.open('catched_url.txt','a','utf-8')
    catched_title_file = codecs.open('catched_title.txt','a','utf-8')
    collect = []
    while URL:
        print("Now queue length is ", len(URL), "    Total ", total)
        catched_url_file.write(URL[0]+'\n')
        try:
            content = getURLContent(URL[0])
        except:
            nothing = True
        else:
            try:
                if len(URL) < maxlen:
                    for url in nextPage(content):
                        if (url in catched_url) == False and url.find('photo') == -1 and url.find('video') == -1:
                            URL.append(url)
                            catched_url[url] = True
                if content.find('<div id="p-detail">') != -1:
                    news = extract(content)
                    if (news['title']+news['time'][:10] in catched_title) == False:
                        collect.append(news)
                        total += 1
                        catched_title[news['title']+news['time'][:10]] = True
                        catched_title_file.write(news['title']+news['time'][:10]+'\n')
                        if total % file_size == 0 and collect:
                            file_id += 1
                            f = codecs.open('data/data_'+str(file_id),'w','utf-8')
                            f.write(json.dumps(collect))
                            f.close()
                            collect = []
                else:
                    print(URL[0])
            except:
                print(URL[0])
        del URL[0]
        # time.sleep(0.5)
    catched_file.close()