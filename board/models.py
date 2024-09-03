# community/board/models.py
from django.db import models
from django.conf import settings

# 게시글 모델: 사용자와 학교에 연결된 게시글 정보
class Board(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey('School', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 댓글 모델: 게시글과 연결된 댓글 정보
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.comment}'

# 학교 모델: 학교에 대한 정보
class School(models.Model):
    city = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return self.school_name if self.school_name else "Unnamed School"
