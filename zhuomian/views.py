# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from zhuomian.models import Image
from image_web import settings

@require_http_methods(['GET','POST'])
def getImage(request):
    title = request.GET.get('title','')

    reslut = Image.objects.filter(title=title)
    data = [{'title': img.title, 'img_url': img.img_url} for img in reslut]

    context = {
        'data': data,
        'title':title
    }
    return render(request=request,template_name='page.html',context=context)


def index(request,count=1):
    count = int(count)
    start = (count - 1) * settings.PAGE_SIZE
    end = count * settings.PAGE_SIZE

    reslut = Image.objects.values('title').annotate(count=Count('img_url')).order_by('-count')[start:end]
    data = [{'title': value['title'], 'count': value['count']} for value in reslut]

    lastPage = count-1 if count > 1 else None
    nextPage = count+1 if len(data) == settings.PAGE_SIZE else None

    context = {
        'data': data,
        'lastPage': lastPage,
        'nextPage': nextPage,
    }

    return render(request=request,template_name='index.html',context=context)
