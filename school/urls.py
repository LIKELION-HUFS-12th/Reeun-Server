# community/member/urls.py

from django.urls import path
from .views import *

app_name = 'school'

urlpatterns = [
    path('getallschool/', GetAllSchoolAPI.as_view(), name='getAllSchool'),  # 등록된 모든 학교의 정보를 가져옴
]
