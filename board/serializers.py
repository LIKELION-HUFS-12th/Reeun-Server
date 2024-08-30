# board/serializers.py

from rest_framework import serializers
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 닉네임을 반환

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at']  # 'user' 필드 추가

class BoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 정보를 읽기 전용으로 설정

    class Meta:
        model = Board
        fields = ['id', 'user', 'title', 'body', 'created_at', 'comments']
from rest_framework import serializers
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 닉네임을 반환
    created_at = serializers.DateTimeField(format='%Y-%m-%d')  # 날짜 형식 지정

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at']  # 'user' 필드 추가

class BoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 정보를 읽기 전용으로 설정
    created_at = serializers.DateTimeField(format='%Y-%m-%d')  # 날짜 형식 지정

    class Meta:
        model = Board
        fields = ['id', 'user', 'title', 'body', 'created_at', 'comments']
