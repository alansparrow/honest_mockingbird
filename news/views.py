from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from .models import News
from datetime import datetime
from django.core import serializers
import json
from django.forms.models import model_to_dict


def index(request):
    return HttpResponse("Hello, world. You're at the news index.")

def get_news(request):
    before_pub_date = request.GET['pub_date'][:19]
    news_count = request.GET['news_count']
    if (news_count.isdigit()):
        news_count = int(news_count)
    else:
        news_count = 20

    before_pub_date = datetime.strptime(before_pub_date, "%Y-%m-%d %H:%M:%S")

    news_list = News.objects.filter(pub_date__lt=before_pub_date).order_by('-pub_date')[:news_count]
    items = []
    for news in news_list:
        items.append(model_to_dict(news))
        
    data = {}
    data['items'] = items

    return JsonResponse(data, safe=False)