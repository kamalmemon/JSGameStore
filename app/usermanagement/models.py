from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_dev = models.BooleanField(default=False, help_text='Designates whether the user is a game developer.')
    email_validated = models.BooleanField(default=False, help_text='User has validated their account with their email.')
