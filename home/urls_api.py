from django.urls import path
from .views_api import *

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
]
