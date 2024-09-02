# community/member/urls.py
from django.urls import path
from .views import (
    UserRegisterView, UserLoginView, UserLogoutView, UserDeleteView,
    UserProfileView, UserProfileUpdateView, SchoolListView
)

app_name = 'member'

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),  # 회원가입
    path('login/', UserLoginView.as_view(), name='login'),  # 로그인
    path('logout/', UserLogoutView.as_view(), name='logout'),  # 로그아웃
    path('delete/', UserDeleteView.as_view(), name='delete'),  # 회원탈퇴
    path('profile/', UserProfileView.as_view(), name='profile'),  # 유저 프로필 조회 및 생성
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),  # 유저 프로필 수정
    path('schools/', SchoolListView.as_view(), name='schools'),  # 학교 목록 조회
]
