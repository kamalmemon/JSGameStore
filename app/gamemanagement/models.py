from django.db import models
from django.conf import settings


class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    url = models.URLField(name='game_url')
    description = models.TextField(max_length=500)
    thumbnail_url = models.URLField(blank=True)
    developer = models.ForeignKey(settings.AUTH_USER_MODEL)  # Game.developer should always be User.isDev == True
    price = models.IntegerField(default=0)
    times_bought = models.IntegerField(default=0)


class Purchase(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    time = models.DateTimeField(auto_now_add=True)


class SaveGame(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    state = models.CharField(max_length=500)


class Score(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    points = models.FloatField(default=0)


class HighScore(models.Model):
    game = models.ForeignKey(Game)
    scores = models.ManyToManyField(Score)  # enforce max 5 for top 5
