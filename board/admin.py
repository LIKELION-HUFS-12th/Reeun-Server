# community/board/admin.py

from django.contrib import admin
from .models import Board, Comment

# 게시글 모델 관리용
class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정
    list_display = ('id', 'user', 'title', 'created_at', 'school', 'admission_year')  # 필드 추가

# 댓글 모델 관리용
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정
    list_display = ('id', 'user', 'board', 'comment', 'created_at')  # 'class_board'를 'board'로 수정

admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
