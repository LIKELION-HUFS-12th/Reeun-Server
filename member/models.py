# community/member/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None  # 이메일 필드 제거
    nickname = models.CharField(max_length=100)  # 닉네임 필드 추가
