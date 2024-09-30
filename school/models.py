from django.db import models

# Create your models here.
# 학교 데이터 외부 입력 모델
class School(models.Model):
    city = models.CharField(max_length=100)  
    school_type = models.CharField(max_length=100) 
    school_name = models.CharField(max_length=100) 

    def __str__(self):
        return self.school_name
