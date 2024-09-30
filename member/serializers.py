# community/member/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Class
from school.serializers import GetSchoolIdAndNameSerializer

User = get_user_model()

# 회원가입 시리얼라이저
class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)  # 비밀번호 입력 필드 
    password2 = serializers.CharField(write_only=True)  # 비밀번호 입력 필드(확인용)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def validate(self, data):
        # 비밀번호 확인
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

# 유저 정보 시리얼라이저
class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# 닉네임만 가져오는 시리얼라이저
class GetNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class UserSetNameClientSerializer(serializers.Serializer):
    name = serializers.CharField()

class UserSetNameServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class UserSetEnrollYearClientSerializer(serializers.Serializer):
    enrollYear = serializers.IntegerField()

class UserSetEnrollYearServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'enrollYear']

class UserSetSchoolClientSerializer(serializers.Serializer):
    schoolId = serializers.IntegerField()

class UserSetSchoolServerSerializer(serializers.ModelSerializer):
    school = GetSchoolIdAndNameSerializer()

    class Meta:
        model = User
        fields = ['id', 'school']

class UserSetClassClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['grade', 'order']

class UserSetClassServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['user', 'grade', 'order', 'isAnonymous']

class UserGetInfoSerializer(serializers.ModelSerializer):
    school = GetSchoolIdAndNameSerializer()
    classList = UserSetClassServerSerializer(many=True, source='class_set')

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'enrollYear', 'school', 'classList']