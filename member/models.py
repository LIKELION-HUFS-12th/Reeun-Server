from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField  # JSONField 임포트

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None  # 이메일 필드 제거
    nickname = models.CharField(max_length=100)  # 닉네임 필드 추가

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    admission_year = models.PositiveIntegerField()
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    
    # 학년 및 반 정보 추가
    grade_1 = models.PositiveIntegerField(null=True, blank=True)
    class_number_1 = models.PositiveIntegerField(null=True, blank=True)
    
    grade_2 = models.PositiveIntegerField(null=True, blank=True)
    class_number_2 = models.PositiveIntegerField(null=True, blank=True)
    
    grade_3 = models.PositiveIntegerField(null=True, blank=True)
    class_number_3 = models.PositiveIntegerField(null=True, blank=True)
    
    grade_4 = models.PositiveIntegerField(null=True, blank=True)
    class_number_4 = models.PositiveIntegerField(null=True, blank=True)
    
    grade_5 = models.PositiveIntegerField(null=True, blank=True)
    class_number_5 = models.PositiveIntegerField(null=True, blank=True)
    
    grade_6 = models.PositiveIntegerField(null=True, blank=True)
    class_number_6 = models.PositiveIntegerField(null=True, blank=True)

    # JSONField로 변경
    grades = JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class School(models.Model):
    city = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)

    def __str__(self):
        return self.school_name
