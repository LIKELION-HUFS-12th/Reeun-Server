# community/classboard/serializers.py

from rest_framework import serializers
from .models import ClassBoard, Comment
from member.models import UserProfile

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
    class_number = serializers.SerializerMethodField()  # 수업 번호

    class Meta:
        model = ClassBoard
        fields = ['id', 'user', 'school_name', 'admission_year', 'grade', 'class_number', 'title', 'body', 'created_at', 'comments']
        extra_kwargs = {'school': {'write_only': True}}  

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else None  # 학교 이름 반환

    def get_grade(self, obj):
        return obj.grade  # 학년 반환

    def get_class_number(self, obj):
        return obj.class_number  # 수업 번호 반환

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"detail": "프로필을 찾을 수 없습니다."})  # 프로필 오류 메시지

        grade = self.context['request'].parser_context['kwargs'].get('grade')
        class_number_field = f'class_number_{grade}'
        class_number = profile.grades.get(f'grade_{grade}', {}).get(class_number_field, None)

        if class_number is None:
            raise serializers.ValidationError({"detail": "주어진 학년에 대해 사용할 수 있는 수업 번호가 없습니다."})  # 해당 학급 오류 메시지

        validated_data['school'] = profile.school
        validated_data['grade'] = grade
        validated_data['class_number'] = class_number
        validated_data['admission_year'] = profile.admission_year

        return super().create(validated_data)
