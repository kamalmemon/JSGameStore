from django.test import TestCase, Client
from django.test.client import RequestFactory
from . import views as gp
from . import utils
from gamemanagement import utils as game_utils
from gamemanagement.models import Game, Purchase
from usermanagement.models import User

# Create your tests here.

class SimpleTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_play_access(self):
        # Adding test form data
        request = self.factory.get('/gamemanagement/play')
        # Creating test player
        test_player = User.objects.create_user('foo', 'myemail@test.com', 'bar', is_dev=False)
        request.user = test_player

        # Creating test developer
        test_dev = User.objects.create_user('foo developer', 'myemaildev@test.com', 'bar', is_dev=True)

        # Creating a test game
        game = Game(title='testGame',
                        game_url='http://www.testUrl.com/t',
                        thumbnail_url='',
                        developer=test_dev,
                        price=20.11,
                        description='test desc')
        game.save()

        # Assigning game to the test player
        purchase = Purchase(game=game,
                            user=request.user)
        purchase.save()

        response = gp.play(request, game.id)
        self.assertEqual(response.status_code, 200, "Access game play")

    def test_highscores_without_post(self):
        request = self.factory.get('/gamemanagement/get_high_scores')

        response = gp.get_high_scores(request)
        self.assertEqual(response.status_code, 405, "Method Not Allowed - without POST requesst")