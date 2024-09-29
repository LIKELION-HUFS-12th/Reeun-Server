# community/board/models.py
# 기본값 설정 바꾸지 말아주세요! 

from django.conf import settings
from django.db import models
from school.models import School

# 게시글 모델
class Board(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    title = models.CharField(max_length=255)  # 제목
    body = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)  # 학교 (기본값 설정)
    admission_year = models.IntegerField(default=0)  # 입학년도

    def __str__(self):
        return self.title

# 댓글 모델
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='board_comments', on_delete=models.CASCADE)  # 작성자
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)  # 게시글
    comment = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일

    def __str__(self):
        return f'Comment by {self.user} on {self.board}'
