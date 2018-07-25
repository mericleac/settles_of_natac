from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^/setup_settlementr1/(?P<settlement_id>\d+)$', views.setup_settlementr1),
    url(r'^/setup_roadr1/(?P<road_id>\d+)$', views.setup_roadr1),
    url(r'^/end_turn', views.end_turn)
]