# community/board/urls.py
from django.urls import path
from .views import *


app_name = 'board'

urlpatterns = [
    # path('', board_list),
    # path('<int:pk>/', board_detail),
    path('', BoardList.as_view()),
    path('<int:pk>/', BoardDetail.as_view()),
]