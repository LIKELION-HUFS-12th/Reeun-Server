# community/board/serializers.py

from rest_framework import serializers
from .models import Board, Comment, School

# 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)  

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at']

# 게시글 시리얼라이저
class BoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), write_only=True)
    school_name = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'user', 'title', 'body', 'created_at', 'school', 'school_name', 'comments']

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else None