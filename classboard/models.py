# community/classboard/models.py

# community/classboard/models.py

from django.conf import settings
from django.db import models
from member.models import School

class ClassBoard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)  # 기본값 설정
    class_number = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)
    admission_year = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_board = models.ForeignKey(ClassBoard, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.class_board}'
