# community/classboard/serializers.py

from rest_framework import serializers
from .models import ClassBoard, Comment
from member.models import CustomUser

class DeleteClassBoardClientSerializer(serializers.Serializer):
    classBoardId = serializers.IntegerField()

class EditClassBoardClientSerializer(serializers.ModelSerializer):
    classBoardId = serializers.IntegerField()

    class Meta:
        model = ClassBoard
        fields = ['classBoardId', 'title', 'body']

class PostClassBoardClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassBoard
        fields = ['grade', 'order', 'admission_year', 'title', 'body']

class PostCommentClientSerializer(serializers.ModelSerializer):
    classBoardId = serializers.IntegerField()
    
    class Meta:
        model = Comment
        fields = ['classBoardId', 'comment']

class EditCommentClientSerializer(serializers.ModelSerializer):
    commentId = serializers.IntegerField()
    
    class Meta:
        model = Comment
        fields = ['commentId', 'comment']

class DeleteCommentClientSerializer(serializers.Serializer):
    commentId = serializers.IntegerField()

# 학급 게시판 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 이름 읽기 전용
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)  # 생성일 읽기 전용
    class_board = serializers.PrimaryKeyRelatedField(queryset=ClassBoard.objects.all(), write_only=True)  # 수업 게시판 ID

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at', 'class_board']

# 학급 게시판 게시글 시리얼라이저
class ClassBoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 관련 댓글
    user = serializers.ReadOnlyField(source='user.username')  # 사용자 이름 읽기 전용
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)  # 생성일 읽기 전용
    school_name = serializers.SerializerMethodField()  # 학교 이름
    grade = serializers.SerializerMethodField()  # 학년
    order = serializers.SerializerMethodField()  # 수업 번호

    class Meta:
        model = ClassBoard
        fields = ['id', 'user', 'school_name', 'admission_year', 'grade', 'order', 'title', 'body', 'created_at', 'comments']
        extra_kwargs = {'school': {'write_only': True}}  

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else None  # 학교 이름 반환

    def get_grade(self, obj):
        return obj.grade  # 학년 반환

    def get_order(self, obj):
        return obj.order  # 수업 번호 반환