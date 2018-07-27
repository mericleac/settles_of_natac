from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'(?P<id>\d+)$', views.index),
    url(r'trade$', views.trade),
    url(r'nvm$', views.nvm),
    url(r'delete$', views.delete),
]