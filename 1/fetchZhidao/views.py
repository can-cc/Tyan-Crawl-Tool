# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import spider
import pylibmc as memcache

def view(request):
    return render_to_response('view.html')

def startFetch(request):
    return HttpResponse(spider.startFetch())

def seezhidaono(request):
    mc = memcache.Client()
    zhidaono = mc.get("zhidaono")
    return HttpResponse(zhidaono)

def start(request):
    return HttpResponse(spider.FetchStart())

def realstart(request):
    spider.fetchzhidao()