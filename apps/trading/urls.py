from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^/(?P<id>\d+)$', views.index),
    url(r'^/create/(?P<id>\d+)$', views.create),
    url(r'^/trade$', views.trade),
    url(r'^/delete$', views.delete),
]