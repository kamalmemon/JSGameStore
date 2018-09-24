from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/games/$', views.games),
    url(r'^v1/game/details/(?P<game_id>[0-9]+)/$', views.game_details),
    url(r'^v1/game/search/(?P<title>[a-zA-Z0-9,.:?!\-\']+)/$', views.game_search),
    url(r'^v1/high_scores/(?P<game_id>[0-9]+)/$', views.high_scores),
    url(r'^v1/dev/(?P<username>[\w.@+-]+)/(?P<password>.+)/statistics/$', views.dev_statistics),
    url(r'^v1/dev/(?P<username>[\w.@+-]+)/(?P<password>.+)/game_sales/(?P<game_id>[0-9]+)/$', views.dev_game_sales),
]
