# community/member/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# 회원가입 시리얼라이저
class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nickname')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

# 사용자 세부 정보 시리얼라이저
class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname']
