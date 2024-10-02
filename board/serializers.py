# community/board/serializers.py

from rest_framework import serializers
from .models import Board, Comment

class PostBoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'body']

class PostCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

# 댓글 데이터 시리얼라이저
class BoardCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 이름 표시
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)  # 생성일 포맷
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), write_only=True, required=False)  # 게시글 참조

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at', 'board']

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

# 게시글 데이터 시리얼라이저
class BoardSerializer(serializers.ModelSerializer):
    comments = BoardCommentSerializer(many=True, read_only=True)  # 댓글 리스트
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 이름 표시
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)  # 생성일 포맷
    school_name = serializers.SerializerMethodField()  # 학교 이름 표시

    class Meta:
        model = Board
        fields = ['id', 'user', 'school_name', 'admission_year', 'title', 'body', 'created_at', 'comments']
        extra_kwargs = {'school': {'write_only': True}} 

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else None

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        validated_data['school'] = user.school
        validated_data['admission_year'] = user.enrollYear

        return super().create(validated_data)
