# community/member/urls.py

from django.urls import path
from .views import *

app_name = 'member'

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),  # 회원가입
    path('login/', UserLoginView.as_view(), name='login'),  # 로그인
    path('logout/', UserLogoutView.as_view(), name='logout'),  # 로그아웃
    path('delete/', UserDeleteView.as_view(), name='delete'),  # 회원탈퇴(사용자 계정 삭제)

    path('setname/', UserSetNameView.as_view(), name='setName'), # 유저의 이름(name) 설정
    path('setenrollyear/', UserSetEnrollYearView.as_view(), name='setEnrollYear'), # 유저의 입학년도(enrollYear) 설정
    path('setschool/', UserSetSchoolView.as_view(), name='setSchool'), # 유저의 학교(school) 설정
    path('setclass/', UserSetClassView.as_view(), name='setClass'), # 유저의 반(Class) 설정
    path('getinfo/', UserGetInfoView.as_view(), name='getInfo'), # 유저 정보 조회

    path('openNicknameToSchool/', OpenNicknameSchoolView.as_view(), name='openNicknameToSchool'), # 자신의 닉네임을 학교에게 공개
    path('openNicknameToClass/', OpenNicknameClassView.as_view(), name='openNicknameToClass'), # 자신의 닉네임을 학급에 공개
    path('getschoolmembers/', UserGetSchoolMemberView.as_view(), name='getSchoolMember'), # 특정 학교의 유저 중 이름공개해둔 멤버 모두 조회
    path('getclassmembers/<int:grade>/', UserGetClassMemberView.as_view(), name='getClassMember'), # 특정 학교의 학년 학급 멤버 이름 공개된 멤버 모두 조회
]
