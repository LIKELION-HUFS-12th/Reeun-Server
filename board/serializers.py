# community/board/serializers.py

from rest_framework import serializers
from .models import Board, Comment
from member.models import UserProfile  

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at', 'board']

class BoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    school_name = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'user', 'school_name', 'admission_year', 'title', 'body', 'created_at', 'comments']
        extra_kwargs = {'school': {'write_only': True}}

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else None

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"detail": "Profile not found."})

        validated_data['school'] = profile.school
        validated_data['admission_year'] = profile.admission_year

        return super().create(validated_data)
