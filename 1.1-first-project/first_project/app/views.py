import os
from datetime import datetime
from datetime import timezone as timez
from tzlocal import get_localzone

from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.utils import timezone

def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.now().strftime('%H:%M:%S')
    return render(request, f"app/timeview.html", {'time': current_time})


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    # raise NotImplemented
    pages = {}
    for item in os.listdir(path='.'):
        pages[item] = reverse('workdir')
    context = {
        'pages': pages
    }
    return render(request, f"app/workdir.html", context)