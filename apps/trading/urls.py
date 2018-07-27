from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'(?P<id>\d+)$', views.index),
    url(r'trade$', views.trade),
    url(r'delete$', views.delete),
    url(r'bank$', views.bank),
    url(r'tradeBank$', views.trade_bank)
]