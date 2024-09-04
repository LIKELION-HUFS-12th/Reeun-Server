# community/board/models.py

from django.conf import settings
from django.db import models
from member.models import School

class Board(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)  # 기본값 설정
    admission_year = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='board_comments', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.board}'
