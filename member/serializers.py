# community/member/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, School

User = get_user_model()

# 유저 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'birth_date', 'admission_year', 'school', 'grades']

# 반 정보 시리얼라이저
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['grades']

    def update(self, instance, validated_data):
        # 전달된 학년 및 반 정보 가져오기
        grades = validated_data.get('grades', {})

        existing_grades = instance.grades or {}
        modified = False

        for grade, class_info in grades.items():
            if grade in existing_grades:
                for class_number_key, class_number_value in class_info.items():
                    # 이미 입력된 값은 수정할 수 없음
                    if existing_grades[grade].get(class_number_key) is not None and class_number_value is not None:
                        raise serializers.ValidationError(
                            f"이미 입력된 값인 {grade}-{class_number_key}는 수정할 수 없습니다."
                        )
                    
                    # 새로 추가된 반 정보는 업데이트
                    if existing_grades[grade].get(class_number_key) is None and class_number_value is not None:
                        existing_grades[grade][class_number_key] = class_number_value
                        modified = True
        
        if modified:
            instance.grades = existing_grades
            instance.save()
        
        return instance

# 회원가입 시리얼라이저
class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)  # 비밀번호 입력 필드 
    password2 = serializers.CharField(write_only=True)  # 비밀번호 입력 필드(확인용)
    nickname = serializers.CharField(max_length=100)  # 닉네임 필드

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nickname')

    def validate(self, data):
        # 비밀번호 확인
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

# 유저 정보 시리얼라이저
class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# 학교 시리얼라이저
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'city', 'school_type', 'school_name']
