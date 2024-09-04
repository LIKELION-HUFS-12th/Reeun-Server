# community/classboard/admin.py

from django.contrib import admin
from .models import ClassBoard, Comment

class ClassBoardAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정
    list_display = ('id', 'user', 'title', 'created_at', 'school', 'class_number', 'grade')  # 필드 추가

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정
    list_display = ('id', 'user', 'class_board', 'comment', 'created_at')  # 'board'를 'class_board'로 수정

admin.site.register(ClassBoard, ClassBoardAdmin)
admin.site.register(Comment, CommentAdmin)
