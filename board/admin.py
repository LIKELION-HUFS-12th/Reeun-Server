# community/board/admin.py
from django.contrib import admin
from .models import Board # 같은 폴더(.) 내에 있는 models모듈에서 Blog를 import해오겠다는 의미입니다. 

# Register your models here.

class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Board, BoardAdmin)