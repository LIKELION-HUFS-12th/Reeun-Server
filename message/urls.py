from django.urls import path
from .views import *

app_name = 'message'

urlpatterns = [
    path('sendMessage/', SendMessageAPI.as_view()),
    path('getMessage/<int:otherId>/', GetMessageAPI.as_view()),
]
