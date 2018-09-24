from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from usermanagement.forms import LoginForm

urlpatterns = [
    url(r'^login/$',
        auth_views.login, {'template_name': 'usermanagement/login.html', 'authentication_form': LoginForm},
        name='login_page'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout_page'),
    url(r'^register/$', views.registration_page, name='registration_page'),
    url(r'^validation/(?P<token>[A-Fa-f0-9]{64})/$', views.email_validation, name='account_validation'),
    url(r'^register_action/$', views.registration_action, name='register_action'),
    url(r'^login_action/$', views.login_action, name='login_action'),
    url(r'^$', RedirectView.as_view(pattern_name='usermanagement:login_page', permanent=False)),
]
