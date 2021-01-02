from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('users/<user_id>', views.users),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]