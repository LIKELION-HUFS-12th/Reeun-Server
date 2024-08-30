# community/member/urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserDeleteView

app_name = 'member'

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('delete/', UserDeleteView.as_view(), name='delete'),
]
