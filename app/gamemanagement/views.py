from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from usermanagement.custom_decorators import user_is_dev, user_is_player
from .models import Game, Purchase, HighScore
from .forms import AddGameForm, EditGameForm
import uuid
from hashlib import md5
from . import utils
from django.contrib import messages
from django.forms.models import model_to_dict


@login_required
def show_personal_page(request):
    if request.user.is_dev:
        games = Game.objects.filter(developer=request.user)
        return render(request, 'gamemanagement/dev.html', context={'games': games})

    if request.GET.get('paymentRedirect') == 'true':
        payment_correct = utils.manage_payment(request)

        if payment_correct:
            messages.success(request, 'Game bought successfully.')
        else:
            messages.error(request, 'Error in purchase, please try again.')

        return HttpResponseRedirect('/home')

    purchases = Purchase.objects.filter(user=request.user)
    available_games = Game.objects.exclude(id__in=[p.game.id for p in purchases])
    return render(request, 'gamemanagement/user.html', context={'purchases': purchases, 'available_games': available_games})


@login_required
@user_is_dev
def add_game(request):
    if request.method == "POST":
        form = AddGameForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            url = form.cleaned_data['url']
            thumbnail_url = form.cleaned_data['imagepath']
            description = form.cleaned_data['description']

            game = Game(title=name,
                        game_url=url,
                        thumbnail_url=thumbnail_url,
                        developer=request.user,
                        price=price,
                        description=description)
            game.save()
            games = Game.objects.filter(developer=request.user)

            messages.success(request, 'Game added successfully.')
            return render(request, 'gamemanagement/dev.html', context={'games': games})

        return render(request, 'gamemanagement/addgame.html', {'form': form})

    form = AddGameForm()
    return render(request, 'gamemanagement/addgame.html', {'form': form})


@login_required
@user_is_dev
def edit_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    form = EditGameForm(initial=model_to_dict(game))
    if game.developer != request.user:
        games = Game.objects.filter(developer=request.user)
        return render(request, 'gamemanagement/dev.html', context={'games': games})

    if request.method == "POST":
        form=EditGameForm(request.POST)
        if form.is_valid():
            game.title = form.cleaned_data['title']
            game.price = form.cleaned_data['price']
            game.game_url = form.cleaned_data['game_url']
            game.thumbnail_url = form.cleaned_data['thumbnail_url']
            game.description = form.cleaned_data['description']
            game.save()

            games = Game.objects.filter(developer=request.user)
            messages.success(request, 'Game edited successfully.')
            return render(request, 'gamemanagement/dev.html', context={'games': games})

        return render(request,'gamemanagement/editgame.html',{'form': form})

    return render(request, 'gamemanagement/editgame.html', context={'form': form})


@login_required
@user_is_dev
def delete_game(request, game_id):
    game = Game.objects.get(pk=game_id)

    if request.user == game.developer:
        game.delete()
        messages.success(request, 'Game deleted successfully.')

    return redirect('gamemanagement:index')


@require_POST
@login_required
#@ajax_required
def payment_gateway_handle(request):
    game_id = request.POST.get('game_id')
    pid = str(uuid.uuid4()) + 'gameid=' + game_id
    amount = Game.objects.get(pk=game_id).price
    sid = 'GGMU2021'
    secret_key = 'aa39e790e5439bf5d51864073507771c'

    checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksum_str.encode("ascii"))
    checksum = m.hexdigest()

    return JsonResponse({'checksum': checksum,
                         'sid': sid,
                         'amount': amount,
                         'pid': pid
                         })


@login_required
@user_is_player
def search(request):
    query = request.GET['q']
    games = Game.objects.filter(title__icontains=query)
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'gamemanagement/searchgame.html', {'query': query, 'games': games, 'purchases': purchases})


@login_required
@user_is_dev
def dev_statistics(request):

    return render(request, 'gamemanagement/dev_statistics.html', context={'stats': utils.get_dev_statistics(request.user)})
