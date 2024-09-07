from django.urls import path
from .views import *

app_name = 'claim'

urlpatterns = [
    path('/makeClaim/', MakeClaimAPI.as_view()),
]
