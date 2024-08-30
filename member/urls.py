# community/member/urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserDeleteView

app_name = 'member'

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),# 회원가입
    path('login/', UserLoginView.as_view(), name='login'), # 로그인
    path('logout/', UserLogoutView.as_view(), name='logout'), # 로그아웃
    path('delete/', UserDeleteView.as_view(), name='delete'), # 회원탈퇴
]
