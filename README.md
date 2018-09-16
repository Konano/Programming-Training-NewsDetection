# NewsDetection

 📚  本次作业实现了一个新闻搜索引擎，包括了使用 Python 搜集网上的新闻和使用 Django 搭建网站服务器。



## Python 抓取新闻

新闻全部来自[新华网](www.xinhuanet.com)。

抓取新闻采用 BFS 的搜索方式，即维护一个待抓取网页队列，每次取出队列头的网址，抓取页面的新闻正文时顺便将其页面上的所有超链接加入到队列尾。

通过调用 request 抓取 html 源码。

通过 bs4 分析 html 源码提取出标签内的信息，将正文储存在 `data` 文件夹内。

通过 jieba 进行正文分词，得到「文章 - 词语」的关系，存入数据库。



## Django 网站服务器

网站的数据库采用内置的 SQLite3 搭建，分为 `News` 和 `Word` 两类，对应关系由前面的 Python 脚本得到。

网站分为 `News` 和 `Search `。

```python
# urls.py

from django.conf.urls import url
import django
from . import page, search

urlpatterns = [
    url(r'^news/$', page.show),
    url(r'^search/$', search.show),
]
```



### 搜索界面

URL:`/search/?w=xxx&p=xxx`

其中 `w` 为搜索语句，`p` 为显示页数（若不存在此参数则默认显示第 1 页）

将搜索语句经过 jieba 分词后，得到多个关键词，在数据库中查找包含这几个关键词的新闻，并按出现次数作为相关度从高到低排序。

接着由显示页数决定显示哪一些新闻，通过 IO 操作读取文件夹 `data` 内的新闻，最后通过修改模板返回数据。

界面 模板&CSS 由 Google 提供（大雾



###展示首页

URL:`/search/?p=xxx`

其中 `p` 为显示页数（若不存在此参数则默认显示第 1 页）

和搜索界面一致，区别在于说搜索栏为空，且显示新闻数量为全部。



### 新闻详情

URL:`/news/?p=xxx`

其中 `p` 为新闻 ID。

通过 IO 操作读取文件夹 `data` 内的新闻，最后通过修改模板返回数据。

新闻底下的新闻推荐显示三条与新闻全文最为相关的其他新闻并提供链接跳转，由后端提前预处理计算完毕。

界面 模板&CSS 由新华网提供（大雾
