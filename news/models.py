from django.db import models
import logging
import hashlib
import uuid
from .shared_info import SharedInfo
from datetime import datetime
import random
# Create your models here.

class FactOpinionVote(models.Model):
    news_id = models.TextField()
    user_token = models.TextField()
    fingerprint = models.TextField()
    vote_type = models.TextField(default=SharedInfo.NEUTRAL)

    def __str__(self):
        return str(self.id) + '   ' + self.news_id + '   ' + \
                    self.user_token + '   ' + self.fingerprint + '   ' + self.vote_type

    @classmethod
    def get(cls, user_token, news_id):
        result = None
        try:
            result = cls.objects.get(user_token=user_token, news_id=news_id)
        except (cls.DoesNotExist, cls.MultipleObjectsReturned) as e:
            print(e)
            result = None

        return result

class TradeVote(models.Model):
    news_id = models.TextField()
    user_token = models.TextField()
    fingerprint = models.TextField()
    vote_type = models.TextField(default=SharedInfo.NEUTRAL_VOTE_TYPE)   # 'neutral', 'hold', 'buy', 'sell'

    def __str__(self):
        return str(self.id) + '   ' + self.news_id + '   ' + \
                    self.user_token + '   ' + self.fingerprint + '   ' + self.vote_type

    @classmethod
    def get(cls, user_token, news_id):
        result = None
        try:
            result = cls.objects.get(user_token=user_token, news_id=news_id)
        except (cls.DoesNotExist, cls.MultipleObjectsReturned) as e:
            print(e)
            result = None

        return result

class UpDownVote(models.Model):
    news_id = models.TextField()
    user_token = models.TextField()
    fingerprint = models.TextField()
    vote_type = models.TextField(default=SharedInfo.NEUTRAL)

    def __str__(self):
        return str(self.id) + '   ' + self.news_id + '   ' + \
                    self.user_token + '   ' + self.fingerprint + '   ' + self.vote_type

    @classmethod
    def get(cls, user_token, news_id):
        result = None
        try:
            result = cls.objects.get(user_token=user_token, news_id=news_id)
        except (cls.DoesNotExist, cls.MultipleObjectsReturned) as e:
            print(e)
            result = None

        return result

class User(models.Model):
    token = models.TextField()

    def __str__(self):
        return str(self.id) + '   ' + self.token

    @classmethod
    def get(cls, token):
        result = None
        try:
            result = cls.objects.get(token=token)
        except cls.DoesNotExist as e:
            print(e)
            result = None

        return result

    @classmethod
    def create_token(cls):
        return str(uuid.uuid4())

class News(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    title = models.TextField()
    url = models.TextField()
    pub_date = models.DateTimeField()
    pub_source = models.TextField()
    fingerprint = models.TextField()
    buy_vote_count = models.IntegerField(default=0)
    sell_vote_count = models.IntegerField(default=0)
    hold_vote_count = models.IntegerField(default=0)
    fact_vote_count = models.IntegerField(default=0)
    opinion_vote_count = models.IntegerField(default=0)
    up_vote_count = models.IntegerField(default=0)
    down_vote_count = models.IntegerField(default=0)
    score = models.FloatField(default=random.uniform(0.1, 0.2))

    def __str__(self):
        return self.title

    @classmethod
    def vote_fact(cls, news_id, vote_count):
        news = cls.get(news_id)
        if (news == None):
            return news

        # vote_count = (1 | -1)
        news.fact_vote_count += vote_count
        if (news.fact_vote_count < 0):
            news.fact_vote_count = 0

        news.save()

        return news

    @classmethod
    def vote_opinion(cls, news_id, vote_count):
        news = cls.get(news_id)
        if (news == None):
            return news

        # vote_count = (1 | -1)
        news.opinion_vote_count += vote_count
        if (news.opinion_vote_count < 0):
            news.opinion_vote_count = 0

        news.save()

        return news

    @classmethod
    def vote_hold(cls, news_id, vote_count):
        news = cls.get(news_id)
        if (news == None):
            return news
        
        # vote_count = (1 | -1)
        news.hold_vote_count += vote_count
        if (news.hold_vote_count < 0):
            news.hold_vote_count = 0
        
        news.save()

        return news

    @classmethod
    def vote_buy(cls, news_id, vote_count):
        news = cls.get(news_id)
        if (news == None):
            return news
        
        # vote_count = (1 | -1)
        news.buy_vote_count += vote_count
        if (news.buy_vote_count < 0):
            news.buy_vote_count = 0
        
        news.save()

        return news

    @classmethod
    def vote_sell(cls, news_id, vote_count):
        news = cls.get(news_id)
        if (news == None):
            return news
        
        # vote_count = (1 | -1)
        news.sell_vote_count += vote_count
        if (news.sell_vote_count < 0):
            news.sell_vote_count = 0
        
        news.save()

        return news


    # calculate score
    @classmethod
    def cal_score(cls, news):
        if (news == None):
            return 0.0

        up_down_diff = news.up_vote_count - news.down_vote_count
        time_diff = (datetime.utcnow() - news.pub_date.replace(tzinfo=None)).total_seconds() / 3600
        score = 0.0
        noise = random.uniform(0.1, 0.2)
        if (up_down_diff - 1 > 0):
            score = (up_down_diff - 1) / ((time_diff + 2) ** SharedInfo.SCORE_GRAVITY)
        else:
            score = (up_down_diff - 1) * ((time_diff + 2) ** SharedInfo.SCORE_GRAVITY)

        score += noise

        return score




    @classmethod
    def vote_up(cls, news_id, vote_count):
        news = cls.get(news_id)
        if (news == None):
            return news

        # vote_count = (1 | -1)
        news.up_vote_count += vote_count
        if (news.up_vote_count < 0):
            news.up_vote_count = 0

        news.score = cls.cal_score(news)
        news.save()

        return news

    @classmethod
    def vote_down(cls, news_id, vote_count):
        news = cls.get(news_id)
        if (news == None):
            return news

        # vote_count = (1 | -1)
        news.down_vote_count += vote_count
        if (news.down_vote_count < 0):
            news.down_vote_count = 0

        news.score = cls.cal_score(news)
        news.save()

        return news

    @classmethod
    def get(cls, news_id):
        result = None
        try:
            result = cls.objects.get(pk=news_id)
        except cls.DoesNotExist as e:
            print(e)
            result = None

        return result

    class Meta:
        managed = True
        db_table = 'news'