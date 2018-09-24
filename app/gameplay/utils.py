from django.http import HttpResponse
from gamemanagement.models import Game
import json


def get_interaction_parameters(request):
    try:
        data = json.loads(request.body)
    except ValueError as error:
        print("invalid json: %s" % error)
        return HttpResponse('invalid json')

    try:
        game_id = int(request.META.get('HTTP_GAME_ID'))
        game = Game.objects.get(id=game_id)
    except TypeError as error:
        print("invalid game id: %s" % error)
        return HttpResponse('invalid game id')

    return data, game, request.user

