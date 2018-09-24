from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .custom_decorators import ajax_required
from usermanagement.custom_decorators import user_is_player
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from gamemanagement import utils as game_utils
from . import utils


@login_required
@user_is_player
def play(request, game_id):
    if not game_id or not game_utils.is_allowed_to_play(request.user,game_id):
        return redirect('/home')

    return render(request, 'gameplay/play.html', context={'game': game_utils.get_game(game_id)})


@require_POST
@login_required
@ajax_required
def handle_game_interaction(request):
    data, game, user = utils.get_interaction_parameters(request)
    message_type = data['messageType']

    if message_type == 'SCORE':
        game_utils.save_score(data, game, user)
    elif message_type == 'SAVE':
        game_utils.save_state(data, game, user)
    elif message_type == 'LOAD_REQUEST':
        return JsonResponse(game_utils.retrieve_state(game, user))

    return HttpResponse('OK')


@require_POST
@login_required
@ajax_required
def get_high_scores(request):
    game_id = request.POST.get('game_id')

    return JsonResponse(game_utils.get_high_score_board(game_id), safe=False)
