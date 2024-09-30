from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .models import School
from .serializers import *

# Create your views here.
class GetAllSchoolAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['학교'],
            operation_summary="모든 학교 조회",
            operation_description="서버 DB에 저장되어 있는 모든 학교의 정보를 가져온다.",
            responses={200: openapi.Response(
                description="조회 성공",
                schema=GetSchoolSerializer(many=True)
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request):
        schoolList = School.objects.all()
        
        serializer = GetSchoolSerializer(schoolList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)