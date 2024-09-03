from django.urls import path
from .views import *

app_name = 'message'

urlpatterns = [
    path('send/', SendMessageAPI.as_view()),
]
