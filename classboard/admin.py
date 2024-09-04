# community/classboard/admin.py

from django.contrib import admin
from .models import ClassBoard, Comment

# 학급 게시판 모델 관리용
class ClassBoardAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정
    list_display = ('id', 'user', 'title', 'created_at', 'school', 'class_number', 'grade')  # 필드 추가

# 학급 댓글 모델 관리용
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정
    list_display = ('id', 'user', 'class_board', 'comment', 'created_at')  # 'class_board' 필드 추가

admin.site.register(ClassBoard, ClassBoardAdmin)
admin.site.register(Comment, CommentAdmin)
