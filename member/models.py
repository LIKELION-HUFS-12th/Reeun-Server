# community/member/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField

#  커스텀 유저 모델
class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []  # 추가 필드 없음
    email = None  # 이메일 필드 제거
    nickname = models.CharField(max_length=100)  # 닉네임 필드 추가

# 사용자 프로필 모델
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  
    full_name = models.CharField(max_length=100)  # 학생 이름
    birth_date = models.DateField()  # 생년월일 
    admission_year = models.PositiveIntegerField()  # 입학 연도 
    school = models.ForeignKey('School', on_delete=models.CASCADE)  # 외래키 연결(학교)
    
    # JSON 필드로 학년 및 반 정보 추가
    grades = JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# 학교 모델(학교 데이터 연결)
class School(models.Model):
    city = models.CharField(max_length=100)  
    school_type = models.CharField(max_length=100) 
    school_name = models.CharField(max_length=100) 

    def __str__(self):
        return self.school_name
