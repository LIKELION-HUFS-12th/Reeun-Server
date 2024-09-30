from rest_framework import serializers
from .models import School

class GetSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'city', 'school_type', 'school_name']

class GetSchoolIdAndNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'school_name']