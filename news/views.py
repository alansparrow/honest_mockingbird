from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from .models import News
from .models import User
from .models import TradeVote
from .models import FactOpinionVote
from datetime import datetime
from django.core import serializers
import json
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .shared_info import SharedInfo



def index(request):
    return HttpResponse("Hello, world. You're at the news index.")

@csrf_exempt
def create_user(request):
    return_data = {}

    if (request.method == 'POST'):
        new_user = User(token = User.create_token())
        new_user.save()
        return_data['new_user'] = model_to_dict(new_user)

    return JsonResponse(return_data, safe=False)

@csrf_exempt
def vote_fact(request):
    return_data = {}

    if (request.method == 'POST'):
        user_token = request.POST['user_token']
        news_id = request.POST['news_id']

        user = User.get(token=user_token)
        news = News.get(news_id=news_id)

        if (user == None or news == None):
            return_data['result_code'] = 1
            return_data['message'] = 'user or news not found'
            return_data['user'] = None
            return_data['news'] = None
        else:
            return_data['result_code'] = 0
            return_data['message'] = 'ok'
            vote = FactOpinionVote.get(user_token=user_token, news_id=news_id)

            if (vote != None):
                if (vote.vote_type != SharedInfo.FACT):
                    if (vote.vote_type == SharedInfo.OPINION):
                        News.vote_opinion(news.id, -1)
                    News.vote_fact(news.id, 1)
                    vote.vote_type = SharedInfo.FACT
                    vote.save()
                else:
                    News.vote_fact(news.id, -1)
                    vote.delete()
            else:
                News.vote_fact(news.id, 1)
                vote = FactOpinionVote(user_token=user_token, news_id=news_id, vote_type=SharedInfo.FACT)
                vote.save()

    return JsonResponse(return_data, safe=False)

@csrf_exempt
def vote_opinion(request):
    return_data = {}

    if (request.method == 'POST'):
        user_token = request.POST['user_token']
        news_id = request.POST['news_id']

        user = User.get(token=user_token)
        news = News.get(news_id=news_id)

        if (user == None or news == None):
            return_data['result_code'] = 1
            return_data['message'] = 'user or news not found'
            return_data['user'] = None
            return_data['news'] = None
        else:
            return_data['result_code'] = 0
            return_data['message'] = 'ok'
            vote = FactOpinionVote.get(user_token=user_token, news_id=news_id)

            if (vote != None):
                if (vote.vote_type != SharedInfo.OPINION):
                    if (vote.vote_type == SharedInfo.FACT):
                        News.vote_fact(news.id, -1)
                    News.vote_opinion(news.id, 1)
                    vote.vote_type = SharedInfo.OPINION
                    vote.save()
                else:
                    News.vote_opinion(news.id, -1)
                    vote.delete()
            else:
                News.vote_opinion(news.id, 1)
                vote = FactOpinionVote(user_token=user_token, news_id=news_id, vote_type=SharedInfo.OPINION)
                vote.save()

    return JsonResponse(return_data, safe=False)

@csrf_exempt
def vote_hold(request):
    return_data = {}

    if (request.method == 'POST'):
        user_token = request.POST['user_token']
        news_id = request.POST['news_id']

        user = User.get(token=user_token)
        news = News.get(news_id=news_id)

        if (user == None or news == None):
            return_data['result_code'] = 1
            return_data['message'] = 'user or news not found'
            return_data['user'] = None
            return_data['news'] = None
        else:
            return_data['result_code'] = 0
            return_data['message'] = 'ok'
            vote = TradeVote.get(user_token=user_token, news_id=news_id)

            if (vote != None):
                if (vote.vote_type != SharedInfo.HOLD_VOTE_TYPE):
                    if (vote.vote_type == SharedInfo.BUY_VOTE_TYPE):
                        News.vote_buy(news.id, -1)
                    elif (vote.vote_type == SharedInfo.SELL_VOTE_TYPE):
                        News.vote_sell(news.id, -1)
                    News.vote_hold(news.id, 1)
                    vote.vote_type = SharedInfo.HOLD_VOTE_TYPE
                    vote.save()
                else:
                    News.vote_hold(news.id, -1)
                    vote.delete()
            else:
                News.vote_hold(news.id, 1)
                vote = TradeVote(user_token=user_token, news_id=news_id, vote_type=SharedInfo.HOLD_VOTE_TYPE)
                vote.save()

    return JsonResponse(return_data, safe=False)


@csrf_exempt
def vote_buy(request):
    return_data = {}

    if (request.method == 'POST'):
        user_token = request.POST['user_token']
        news_id = request.POST['news_id']

        user = User.get(token=user_token)
        news = News.get(news_id=news_id)

        if (user == None or news == None):
            return_data['result_code'] = 1
            return_data['message'] = 'user or news not found'
            return_data['user'] = None
            return_data['news'] = None
        else:
            return_data['result_code'] = 0
            return_data['message'] = 'ok'
            vote = TradeVote.get(user_token=user_token, news_id=news_id)

            if (vote != None):
                if (vote.vote_type != SharedInfo.BUY_VOTE_TYPE):
                    if (vote.vote_type == SharedInfo.HOLD_VOTE_TYPE):
                        News.vote_hold(news.id, -1)
                    elif (vote.vote_type == SharedInfo.SELL_VOTE_TYPE):
                        News.vote_sell(news.id, -1)
                    News.vote_buy(news.id, 1)
                    vote.vote_type = SharedInfo.BUY_VOTE_TYPE
                    vote.save()
                else:
                    News.vote_buy(news.id, -1)
                    vote.delete()
            else:
                News.vote_buy(news.id, 1)
                vote = TradeVote(user_token=user_token, news_id=news_id, vote_type=SharedInfo.BUY_VOTE_TYPE)
                vote.save()

    return JsonResponse(return_data, safe=False)

@csrf_exempt
def vote_sell(request):
    return_data = {}

    if (request.method == 'POST'):
        user_token = request.POST['user_token']
        news_id = request.POST['news_id']

        user = User.get(token=user_token)
        news = News.get(news_id=news_id)

        if (user == None or news == None):
            return_data['result_code'] = 1
            return_data['message'] = 'user or news not found'
            return_data['user'] = None
            return_data['news'] = None
        else:
            return_data['result_code'] = 0
            return_data['message'] = 'ok'
            vote = TradeVote.get(user_token=user_token, news_id=news_id)

            if (vote != None):
                if (vote.vote_type != SharedInfo.SELL_VOTE_TYPE):
                    if (vote.vote_type == SharedInfo.HOLD_VOTE_TYPE):
                        News.vote_hold(news.id, -1)
                    elif (vote.vote_type == SharedInfo.BUY_VOTE_TYPE):
                        News.vote_buy(news.id, -1)
                    News.vote_sell(news.id, 1)
                    vote.vote_type = SharedInfo.SELL_VOTE_TYPE
                    vote.save()
                else:
                    News.vote_sell(news.id, -1)
                    vote.delete()
            else:
                News.vote_sell(news.id, 1)
                vote = TradeVote(user_token=user_token, news_id=news_id, vote_type=SharedInfo.SELL_VOTE_TYPE)
                vote.save()

    return JsonResponse(return_data, safe=False)
    
def get_news(request):
    return_data = {}

    if (request.method == 'GET'):
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


        return_data['items'] = items

    return JsonResponse(return_data, safe=False)
