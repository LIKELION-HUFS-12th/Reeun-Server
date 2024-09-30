# community/member/urls.py

from django.urls import path
from .views import *

app_name = 'member'

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),  # 회원가입
    path('login/', UserLoginView.as_view(), name='login'),  # 로그인
    path('logout/', UserLogoutView.as_view(), name='logout'),  # 로그아웃
    path('delete/', UserDeleteView.as_view(), name='delete'),  # 회원탈퇴(사용자 계정 삭제)
    path('profile/', UserProfileView.as_view(), name='user_profile'),  # 유저 정보 조회 및 생성
    path('grades/', GradeView.as_view(), name='grade_view'),  # 반 정보 조회 및 수정

    path('setname/', UserSetNameView.as_view(), name='setName'), # 유저의 이름(name) 설정
    path('setenrollyear/', UserSetEnrollYearView.as_view(), name='setEnrollYear'), # 유저의 입학년도(enrollYear) 설정
    path('setschool/', UserSetSchoolView.as_view(), name='setSchool'), # 유저의 학교(school) 설정
    path('setclass/', UserSetClassView.as_view(), name='setClass') # 유저의 반(Class) 설정

]
