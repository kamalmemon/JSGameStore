from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from usermanagement.models import User
from django.core.mail import send_mail
from . import utils
from django.urls import reverse
from django.contrib import messages


@require_POST
def login_action(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        return redirect('/home')
    else:
        # Return an 'invalid login' error message.
        form = LoginForm()
        return render(request, 'usermanagement/login.html', {'form': form, 'login_error': True})


def registration_page(request):
    form = RegistrationForm()
    return render(request, 'usermanagement/registration.html', {'form': form})


@require_POST
def registration_action(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        is_dev = form.cleaned_data['is_dev']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirmPassword']
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'usermanagement/registration.html', {'form': form, 'user_already_exists': True})
        if not password or password != confirm_password:
            return render(request, 'usermanagement/registration.html', {'form': form, 'password_mismatch': True})

        u = User.objects.create_user(first_name=name, email=email, is_dev=is_dev, username=username, password=password)
        u.save()

        user = authenticate(request, username=username, password=password)
        login(request, user)

        val_url = request.get_host() + reverse('usermanagement:account_validation', args=[utils.token_generator(username, email)])
        send_mail('Registration completed',
                  'Thank you for registering into JSGameStore! Please visit this link to validate your account ' + val_url,
                  'hello@JSGameStore.com',
                  [email])

        return redirect('/home')


@login_required
def email_validation(request, token):
    if token == utils.token_generator(request.user.username, request.user.email):
        u = request.user
        u.email_validated = True
        u.save()
        messages.success(request, 'Account validated successfully')
    else:
        messages.error(request, 'Error validating account')

    return redirect('/home')
