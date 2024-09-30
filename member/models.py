# community/member/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField
from school.models import School

#  커스텀 유저 모델
class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []  # 추가 필드 없음

    email = None  # 이메일 필드 제거
    last_login = None
    is_superuser = None
    first_name = None
    last_name = None
    is_staff = None

    createDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=True, blank=True, max_length=10)
    enrollYear = models.CharField(null=True, blank=True, max_length=4)
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE)

# 유저가 소속된 반
class Class(models.Model):
    school = models.ForeignKey(School, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    grade = models.IntegerField(max_length=1) # 몇학년인지 (1 ~ 6)
    order = models.IntegerField(max_length=2) # 몇반인지 (1 ~ 10)
    isAnonymous = models.BooleanField();

# # 사용자 프로필 모델
# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  
#     full_name = models.CharField(max_length=100)  # 학생 이름
#     birth_date = models.DateField()  # 생년월일 
#     admission_year = models.PositiveIntegerField()  # 입학 연도 
#     school = models.ForeignKey('UserSchool', on_delete=models.CASCADE)  # 외래키 연결(학교)
    
#     # JSON 필드로 학년 및 반 정보 추가
#     grades = JSONField(null=True, blank=True)

#     def __str__(self):
#         return f'{self.user.username} Profile'

# # 학교 모델(학교 데이터 연결)
# class UserSchool(models.Model):
#     city = models.CharField(max_length=100)  
#     school_type = models.CharField(max_length=100) 
#     school_name = models.CharField(max_length=100) 

#     def __str__(self):
#         return self.school_name
