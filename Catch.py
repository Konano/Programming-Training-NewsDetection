# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 00:47:45
# @Last Modified by:   Konano
# @Last Modified time: 2018-09-11 11:25:59

import urllib.request
import re
import time
import os
import codecs

# import chardet

maxlen = 100
total = 0

def getURLContent(url):
    print ("getURLContent: ", url)
    while True:
        flag = 1;
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib.request.Request(url = url, headers = headers);
            content = urllib.request.urlopen(req, timeout = 10).read();
        except:
            print ('get content Error:', url)
            flag = 0;
            time.sleep(5)
        if flag == 1:
            break;
    return content.decode('utf-8','ignore')

def store(content):
    global total
    total = total + 1
    f = codecs.open(str(total)+'.htm','w','utf-8')
    f.write(content)
    f.close()

def nextPage(content):
    p = re.compile(r'http://www.xinhuanet.com/[\/\-\w]+.htm')
    return p.findall(content)

if __name__ == '__main__':
    URL = ['http://www.xinhuanet.com/index.htm']
    while URL:
        print("Now queue length is ", len(URL))
        content = getURLContent(URL[0])
        del URL[0]
        # if isNews(content):
        store(content)
        if len(URL) < maxlen:
            URL.extend(nextPage(content))