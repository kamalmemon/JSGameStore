from django.test import TestCase, Client
from django.test.client import RequestFactory
from . import views as um
from .models import User
from .forms import LoginForm, RegistrationForm
from . import utils

class SimpleTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_registration_form(self):
        # Adding test form data
        form_data = {'name': 'testPlayer',
                        'email': 'test@servertest.com',
                        'is_dev': False,
                        'username': 'testUser',
                        'password': 'testPass',
                        'confirmPassword': 'testPass',
                    }

        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_login_form(self):
        # Adding test form data
        form_data = {'username': 'testUser',
                     'password': 'testPass'
                    }

        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_rendering(self):
        request = self.factory.get('/usermanagement/registration_page')

        response = um.registration_page(request)
        self.assertEqual(response.status_code, 200, "Render registeration page")

    def test_registration_rendering(self):
        request = self.factory.get('/usermanagement/registration_page')

        response = um.registration_page(request)
        self.assertEqual(response.status_code, 200, "Render registeration page")
