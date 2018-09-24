from django.test import TestCase, Client
from django.test.client import RequestFactory
from . import views as gm
from usermanagement.models import User
from .models import Game
from .forms import AddGameForm

class SimpleTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_addgame_form(self):
        # Adding test form data
        form_data = {'name': 'testGame',
                        'price': 22,
                        'url': 'http://testurl.com/testgame',
                        'imagepath': 'testImagePath',
                        'description': 'test desc',
                    }
        form = AddGameForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_addgame_rendering(self):
        request = self.factory.get('/gamemanagement/add_game')
        # Creating test developer
        test_dev = User.objects.create_user('foo', 'myemail@test.com', 'bar', is_dev=True)
        request.user = test_dev

        response = gm.add_game(request)
        self.assertEqual(response.status_code, 200, "Add Game template for developer")
    
    def test_editgame_rendering(self):
        request = self.factory.get('/gamemanagement/edit')
        # Creating test developer
        test_dev = User.objects.create_user('foo', 'myemail@test.com', 'bar', is_dev=True)
        request.user = test_dev
        # Creating test game
        game = Game(title='testGame',
                        game_url='testUrl',
                        thumbnail_url='',
                        developer=request.user,
                        price=20.11,
                        description='test desc')
        game.save()

        response = gm.edit_game(request, game.id)
        self.assertEqual(response.status_code, 200, "Edit Game template for developer")
    
    def test_statistics_rendering(self):
        request = self.factory.get('/gamemanagement/dev_statistics')
        # Creating test developer
        test_dev = User.objects.create_user('foo', 'myemail@test.com', 'bar', is_dev=True)
        request.user = test_dev

        response = gm.dev_statistics(request)
        self.assertEqual(response.status_code, 200, "Game statistics template for developer")

    def test_forms_access(self):
        request = self.factory.get('/gamemanagement/add_game')
        # Creating a player user
        test_dev = User.objects.create_user('foo', 'myemail@test.com', 'bar', is_dev=False)
        request.user = test_dev

        response = gm.add_game(request)
        self.assertEqual(response.status_code, 302, "Forbidden: User is not a developer")