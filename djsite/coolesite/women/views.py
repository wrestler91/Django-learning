from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

# Create your views here.
def index(request): # request - HttpRequest
    return HttpResponse('Страница приложения women.')

def categories(request, categ):
    if (request.GET):
        print(request.GET)
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{categ}</p>')

def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
