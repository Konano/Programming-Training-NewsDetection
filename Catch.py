# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 00:47:45
# @Last Modified by:   Konano
# @Last Modified time: 2018-09-11 12:09:40

import urllib.request
import re
import time
import os
import codecs

# import chardet

maxlen = 1000
total = 0
path = 'E:/tmp/htm/'
path_fail = 'E:/tmp/htm_fail/'

d = {}

def getURLContent(url):
    print ("getURLContent: ", url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url = url, headers = headers)
    content = urllib.request.urlopen(req, timeout = 10).read()
    return content.decode('utf-8','ignore')

def store(url,content):
    global total
    if content.find('<div id="p-detail">') != -1:
        # 如果是新闻的话
        total += 1
        f = codecs.open(path+url.replace('/','.').replace(':',''),'w','utf-8')
        f.write(content)
        f.close()
    else:
        # 如果不是新闻的话
        f = codecs.open(path_fail+url.replace('/','.').replace(':',''),'w','utf-8')
        f.write(content)
        f.close()

def nextPage(content):
    p = re.compile(r'http://www.xinhuanet.com/[\/\-\w]+.htm')
    return p.findall(content)

if __name__ == '__main__':
    URL = ['http://www.xinhuanet.com/index.htm']
    while URL and total < 1000:
        print("Now queue length is ", len(URL))
        if URL[0] in d:
            del URL[0]
            continue
        try:
            content = getURLContent(URL[0])
            store(URL[0],content)
            d[URL[0]] = True
            if len(URL) < maxlen:
                URL.extend(nextPage(content))
        except:
            print("Error!")
        del URL[0]
        time.sleep(0.5)