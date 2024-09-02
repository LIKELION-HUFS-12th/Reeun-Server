from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, School

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

# 학교 시리얼라이저
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'city', 'school_type', 'school_name']

# 유저 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), required=True)
    grades = serializers.JSONField(required=False, allow_null=True, default=dict)

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'birth_date', 'admission_year', 'school', 'grades'
        ]

    def create(self, validated_data):
        grades = validated_data.pop('grades', {})
        user_profile = UserProfile.objects.create(**validated_data)
        user_profile.grades = self.normalize_grades(grades)
        user_profile.save()
        return user_profile

    def update(self, instance, validated_data):
        grades = validated_data.pop('grades', {})

        # 수정할 수 없는 항목 확인
        invalid_updates = {}
        for grade, class_info in grades.items():
            if grade in instance.grades:
                for class_number_key, class_number_value in class_info.items():
                    if instance.grades[grade].get(class_number_key) is not None and class_number_value is not None:
                        invalid_updates[f"{grade} - {class_number_key}"] = "이미 값이 있는 항목은 수정할 수 없습니다."
        
        if invalid_updates:
            raise serializers.ValidationError(invalid_updates)
        
        # 수정 가능한 항목 업데이트
        for field in ['full_name', 'birth_date', 'admission_year', 'school']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        
        # 성적 처리
        existing_grades = instance.grades or {}
        new_grades = self.normalize_grades(grades)
        
        # 기존 성적이 null인 경우만 업데이트
        for grade, class_info in new_grades.items():
            if grade in existing_grades:
                for class_number_key, class_number_value in class_info.items():
                    if existing_grades[grade].get(class_number_key) is None and class_number_value is not None:
                        existing_grades[grade][class_number_key] = class_number_value
        
        instance.grades = existing_grades
        instance.save()
        return instance

    def normalize_grades(self, grades):
        # 모든 학년 (1부터 6까지)이 포함되도록 보장하고, 누락된 학년은 {'class_number_X': None}으로 설정
        normalized_grades = {}
        for i in range(1, 7):
            grade_key = f'grade_{i}'
            if grade_key in grades:
                # 클래스 번호가 없으면 None으로 설정
                normalized_grades[grade_key] = {
                    f'class_number_{i}': grades[grade_key].get(f'class_number_{i}', None)
                }
            else:
                # 학년이 누락된 경우, null 값으로 생성
                normalized_grades[grade_key] = {
                    f'class_number_{i}': None
                }
        return normalized_grades
