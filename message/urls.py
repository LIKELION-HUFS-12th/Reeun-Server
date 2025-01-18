from django.urls import path
from .views import *

app_name = 'message'

urlpatterns = [
    path('', GetMemberAPI.as_view()),
    path('sendMessage/', SendMessageAPI.as_view()),
    path('getMessage/<int:otherId>/', GetMessageAPI.as_view()),
    path('exitMessage/', ExitMessageAPI.as_view()),
]
