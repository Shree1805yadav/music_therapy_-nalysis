from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup', Signup, name='signup'),
    path("", index, name="home"),
    path("about", about, name="about"),
    path("contact", contact, name='contact'),
    path('login', LoginUser, name='login'),
    path('logout', Logout),
    path('form', Form),
    path('casepaper', casePaper),
    path("review/<int:pk>", review, name="review"),
    path("table", recom, name="recom"),

    # email
    path(r'^account_activation_sent/$', views.account_activation_sent,
         name='account_activation_sent'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
    path(r'^account_activation_sent/$', views.account_activation_sent,
         name='account_activation_sent'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
    
      path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete')
    
]
