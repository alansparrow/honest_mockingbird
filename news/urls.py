from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get$', views.get_news),
    url(r'^user/create$', views.create_user),
    url(r'^vote/hold$', views.vote_hold),
    url(r'^vote/buy$', views.vote_buy),
    url(r'^vote/sell$', views.vote_sell),
    url(r'^vote/fact$', views.vote_fact),
    url(r'^vote/opinion$', views.vote_opinion),
    url(r'^vote/up$', views.vote_up),
    url(r'^vote/down$', views.vote_down)
]