from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .models import School
from .serializers import *

# Create your views here.
class GetAllSchoolAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        schoolList = School.objects.all()
        
        serializer = GetSchoolSerializer(schoolList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)