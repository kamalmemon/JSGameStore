from django.http import JsonResponse, HttpResponse
from django.core import serializers
from gamemanagement.models import Game, HighScore, Purchase
from . import utils
import gamemanagement.utils as game_utils


def games(request):
    try:
        offset, limit = utils.get_pagination_params(request)
    except utils.PaginationParamsError as e:
        return e.json_response

    gs = serializers.serialize('json', Game.objects.all()[offset:limit])

    return HttpResponse(gs, content_type='application/json')


def game_details(request, game_id):
    try:
        g = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({
            'status': 'ERROR',
            'message': 'Game not found'
        })

    serialized_g = serializers.serialize('json', [g, ])
    return HttpResponse(serialized_g, content_type='application/json')


def game_search(request, title):
    try:
        offset, limit = utils.get_pagination_params(request)
    except utils.PaginationParamsError as e:
        return e.json_response

    gs = serializers.serialize('json', Game.objects.filter(title__icontains=title)[offset:limit])
    return HttpResponse(gs, content_type='application/json')


def high_scores(request, game_id):
    try:
        hs = HighScore.objects.get(game=game_id)
    except HighScore.DoesNotExist:
        return JsonResponse({
            'status': 'ERROR',
            'message': 'Game not found.'
        })

    serialized_hs = serializers.serialize('json', [hs, ])
    return HttpResponse(serialized_hs, content_type='application/json')


def dev_statistics(request, username, password):
    try:
        offset, limit = utils.get_pagination_params(request)
    except utils.PaginationParamsError as e:
        return e.json_response

    try:
        u = utils.authenticate_user(username, password)
    except utils.UserError as e:
        return e.json_response

    return JsonResponse(game_utils.get_dev_statistics(u)[offset:limit], safe=False)


def dev_game_sales(request, username, password, game_id):
    try:
        offset, limit = utils.get_pagination_params(request)
    except utils.PaginationParamsError as e:
        return e.json_response

    try:
        u = utils.authenticate_user(username, password)
    except utils.UserError as e:
        return e.json_response

    if not Game.objects.filter(id=game_id).exists() or Game.objects.get(id=game_id).developer != u:
        return JsonResponse({
            'status': 'ERROR',
            'message': 'Permission denied.'
        })

    ps = Purchase.objects.filter(game=game_id)[offset:limit]

    serialized_ps = serializers.serialize('json', ps)
    return HttpResponse(serialized_ps, content_type='application/json')
