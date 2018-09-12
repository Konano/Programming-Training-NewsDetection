# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-11 22:42:49
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-12 10:16:00

from django.shortcuts import render

def mainpage(request):
    return render(request, 'index.html')