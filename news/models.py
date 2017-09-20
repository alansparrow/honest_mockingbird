from django.db import models

# Create your models here.

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

    class Meta:
        managed = True
        db_table = 'news'