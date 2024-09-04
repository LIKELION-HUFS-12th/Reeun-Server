# community/classboard/serializers.py

# community/classboard/serializers.py

from rest_framework import serializers
from .models import ClassBoard, Comment
from member.models import UserProfile

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    class_board = serializers.PrimaryKeyRelatedField(queryset=ClassBoard.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at', 'class_board']

class ClassBoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    school_name = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    class_number = serializers.SerializerMethodField()

    class Meta:
        model = ClassBoard
        fields = ['id', 'user', 'school_name', 'admission_year', 'grade', 'class_number', 'title', 'body', 'created_at', 'comments']
        extra_kwargs = {'school': {'write_only': True}}

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else None

    def get_grade(self, obj):
        return obj.grade

    def get_class_number(self, obj):
        return obj.class_number

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"detail": "Profile not found."})

        grade = self.context['request'].parser_context['kwargs'].get('grade')
        class_number_field = f'class_number_{grade}'
        class_number = profile.grades.get(f'grade_{grade}', {}).get(class_number_field, None)

        if class_number is None:
            raise serializers.ValidationError({"detail": "No class number available for the given grade."})

        validated_data['school'] = profile.school
        validated_data['grade'] = grade
        validated_data['class_number'] = class_number
        validated_data['admission_year'] = profile.admission_year

        return super().create(validated_data)
