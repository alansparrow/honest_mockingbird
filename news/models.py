from django.db import models
import logging
import hashlib
import uuid
# Create your models here.

class Vote(models.Model):
    news_id = models.TextField()
    user_token = models.TextField()
    fingerprint = models.TextField()
    vote_type = models.TextField(default='neutral')   # 'neutral', 'hold', 'buy', 'sell'

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
    title = models.TextField()
    url = models.TextField()
    pub_date = models.DateTimeField()
    pub_source = models.TextField()
    fingerprint = models.TextField()
    buy_vote_count = models.IntegerField(default=0)
    sell_vote_count = models.IntegerField(default=0)
    hold_vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

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