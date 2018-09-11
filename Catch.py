# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 00:47:45
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-11 21:20:17

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
file_id = 7

d = {}
URL = []
# URL = ['http://www.xinhuanet.com/index.htm']
# URL = ['http://www.xinhuanet.com/2018-05/22/c_1122870950.htm']

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
    dict_file = codecs.open('dict.txt','r','utf-8')
    dict_log = dict_file.readlines()
    dict_file.close()
    for i in dict_log:
        d[i] = True
    while len(URL) < maxlen:
        try:
            content = getURLContent(random.choice(dict_log))
        except:
            nothing = True
        else:
            for i in nextPage(content):
                if (i in d) == False and i.find('photo') == -1 and i.find('video') == -1:
                    URL.append(i)
                    d[i] = True

    dict_file = codecs.open('dict.txt','a','utf-8')
    collect = []
    while URL:
        print("Now queue length is ", len(URL), "    Total ", total)
        dict_file.write(URL[0]+'\n')
        try:
            content = getURLContent(URL[0])
        except:
            nothing = True
        else:
            try:
                if len(URL) < maxlen:
                    for i in nextPage(content):
                        if (i in d) == False and i.find('photo') == -1 and i.find('video') == -1:
                            URL.append(i)
                            d[i] = True
                if content.find('<div id="p-detail">') != -1:
                    collect.append(extract(content))
                    total += 1
                    if total % file_size == 0 and collect:
                        file_id += 1
                        f = codecs.open('data/date_'+str(file_id),'w','utf-8')
                        f.write(json.dumps(collect))
                        f.close()
                        collect = []
                else:
                    print(URL[0])
            except:
                print(URL[0])
        del URL[0]
        time.sleep(0.5)
    dict_file.close()