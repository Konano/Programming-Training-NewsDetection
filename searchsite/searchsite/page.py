# -*- coding: utf-8 -*-
# @Author: NanoApe
# @Date:   2018-09-12 09:48:09
# @Last Modified by:   NanoApe
# @Last Modified time: 2018-09-12 14:27:17

from django.shortcuts import render

def show(request):
	context          = {}
	context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)