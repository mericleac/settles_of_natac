from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'roll_dice$', views.roll_dice),
    url(r'purchase_settlement/(?P<settlement_id>\d+)', views.purchase_settlement),
]