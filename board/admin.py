# board/admin.py

from django.contrib import admin
from .models import Board, Comment

class BoardAdmin(admin.ModelAdmin):
    # 실제 모델에서 존재하는 필드를 참조해야 합니다.
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정

    list_display = ('title', 'user', 'created_at')  # 리스트에 표시할 필드

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)  # 'created_at' 필드를 읽기 전용으로 설정

    list_display = ('board', 'user', 'comment', 'created_at')  # 리스트에 표시할 필드

admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
