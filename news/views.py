from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from .models import News
from datetime import datetime
from django.core import serializers


def index(request):
    return HttpResponse("Hello, world. You're at the news index.")

def get_news(request):
    before_pub_date = request.GET['pub_date'][:19]
    before_pub_date = datetime.strptime(before_pub_date, "%Y-%m-%d %H:%M:%S")

    news_list = News.objects.filter(pub_date__lte=before_pub_date)[:20]

    data = serializers.serialize('json', news_list)
    return JsonResponse(data, safe=False)