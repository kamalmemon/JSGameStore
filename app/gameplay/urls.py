from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<game_id>[0-9]*)$', views.play, name='play'),
    url(r'^game-state$', views.handle_game_interaction, name='post_game_state'),
    url(r'^get-high-scores$', views.get_high_scores, name='get_high_scores'),
]
