# community/classboard/models.py

from django.conf import settings
from django.db import models
from school.models import School

# 학급게시판 게시글  모델
class ClassBoard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    title = models.CharField(max_length=255)  # 제목
    body = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)  # 학교
    grade = models.IntegerField(default=0)  # 학년
    order = models.IntegerField(default=0)  # 수업 번호
    admission_year = models.IntegerField(default=0)  # 입학 연도

    def __str__(self):
        return self.title

# 학급게시판 댓글 모델
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    class_board = models.ForeignKey(ClassBoard, related_name='comments', on_delete=models.CASCADE)  
    comment = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f'Comment by {self.user} on {self.class_board}'
