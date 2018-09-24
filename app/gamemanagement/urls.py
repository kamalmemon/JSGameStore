from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_personal_page, name='index'),
    url(r'^add$', views.add_game, name='add_game'),
    url(r'^edit/(?P<game_id>[0-9]+)/$', views.edit_game, name='edit_game'),
    url(r'^delete/(?P<game_id>[0-9]+)/$', views.delete_game, name='delete_game'),
    url(r'^buy$', views.payment_gateway_handle, name='buy_game'),
    url(r'^search/$', views.search, name='search'),
    url(r'^statistics/$', views.dev_statistics, name='dev_statistics'),
]
