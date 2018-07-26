from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'roll_dice$', views.roll_dice),
    url(r'setup$', views.setup),
    url(r'player_turn$', views.player_turn),
    url(r'purchase_settlement/(?P<settlement_id>\d+)', views.purchase_settlement),
    url(r'settlement/(?P<settlement_id>\d+)', views.settlement),
    url(r'purchase_road/(?P<road_id>\d+)', views.purchase_road),
    url(r'initialize_db$', views.initialize_db),
    url(r'road/(?P<road_id>\d+)', views.road),
    url(r'end_turn', views.player_turn),
    url(r'resources', views.resources),
    url(r'clear', views.clear),
    url(r'victory/(?P<player_id>\d+)', views.victory)
]