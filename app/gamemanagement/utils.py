from .models import SaveGame, Score, HighScore, Game, Purchase
from django.shortcuts import get_object_or_404
import json
from hashlib import md5


def save_score(data, game, user):
    score_points = data['score']
    score = Score(game=game, user=user, points=score_points)
    score.save()

    game_board = HighScore.objects.get_or_create(game=game)[0]

    if game_board.scores.count() < 5:
        game_board.scores.add(score)  # no need to .save()
    else:
        if game_board.scores.filter(points__lt=score.points).exists():
            worst = game_board.scores.order_by('points')[0]
            game_board.scores.remove(worst)

            game_board.scores.add(score)

    delete_state(game, user)


def save_state(data, game, user):
    if SaveGame.objects.filter(game=game, user=user).exists():
        save_game = SaveGame.objects.get(game=game, user=user)
        save_game.state = json.dumps(data['gameState'])
    else:
        save_game = SaveGame(game=game, user=user, state=json.dumps(data['gameState']))

    save_game.save()


def retrieve_state(game, user):
    if SaveGame.objects.filter(game=game, user=user).exists() and SaveGame.objects.filter(game=game, user=user).count() == 1:
        save_game = SaveGame.objects.get(game=game, user=user)
        message = {
            "messageType": "LOAD",
            "gameState": json.loads(save_game.state)
        }
    else:
        message = {
            "messageType": "ERROR",
            "info": "Gamestate could not be loaded"
        }

    return message


def delete_state(game, user):
    if SaveGame.objects.filter(game=game, user=user).exists():
        save_game = SaveGame.objects.get(game=game, user=user)
        save_game.delete()

        return True

    return False


def query_transform(request, param_list, **kwargs):
    updated = request.GET.copy()
    # for k, v in kwargs.iteritems():
    #     updated[k] = v

    for param in param_list:
        try:
            del updated[param]
        except KeyError:
            pass

    return updated.urlencode()


def is_allowed_to_play(user, game_id):
    return Purchase.objects.filter(user=user).filter(game=game_id).exists()


def has_game(user, game):
    return Purchase.objects.filter(user=user).filter(game=game).exists()


def manage_payment(request):
    if request.GET.get('result') == 'success':
        pid = request.GET.get('pid')
        ref = request.GET.get('ref')
        result = request.GET.get('result')
        secret_key = 'aa39e790e5439bf5d51864073507771c'

        checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
        m = md5(checksum_str.encode("ascii"))
        checksum = m.hexdigest()

        if checksum == request.GET.get('checksum'):
            game_id = pid.split("gameid=")[1]

            if not has_game(request.user, game_id):
                game = Game.objects.get(pk=game_id)
                purchase = Purchase(game=game,
                                    user=request.user)
                purchase.save()

                game.times_bought += 1
                game.save()

            return True

    return False


def get_high_score_board(game_id):
    game = get_object_or_404(Game, id=game_id)
    high_scores = HighScore.objects.get(game=game).scores.order_by('-points')

    high_scores_board = []
    for hs in high_scores:
        high_scores_board.append({'points': hs.points, 'username': hs.user.username})

    return high_scores_board


def get_game(game_id):
    return get_object_or_404(Game, id=game_id)


def get_dev_statistics(dev):
    stats = []
    games = Game.objects.filter(developer=dev)

    for game in games:
        hs = None
        ltb = None
        if HighScore.objects.filter(game=game).exists() and HighScore.objects.get(game=game).scores.exists():
            hs = HighScore.objects.get(game=game).scores.order_by('-points')[0].points
        if Purchase.objects.filter(game=game).exists():
            ltb = Purchase.objects.filter(game=game).order_by('-time')[0].time

        s = {
            'title': game.title,
            'times_bought': game.times_bought,
            'price': game.price,
            'best_score': hs,
            'last_time_bought': ltb,
        }
        stats.append(s)

    return stats
