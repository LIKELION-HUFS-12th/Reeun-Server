# community/member/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from dj_rest_auth.views import LoginView
from .models import Class
from school.models import School

User = get_user_model()

# 회원가입
class UserRegisterView(APIView):
    permission_classes = [AllowAny]  # 모든 사용자에게 접근 허용

    def post(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class UserLoginView(LoginView):
    permission_classes = [AllowAny]  # 모든 사용자에게 접근 허용

# 로그아웃
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 허용

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)  # 로그아웃 시 모든 토큰을 블랙리스트에 추가
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 허용

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")
        if user.check_password(password):
            user.delete()  # 비밀번호 확인 후 사용자 삭제
            return Response({"detail": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
class UserSetNameView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['유저 정보'],
            operation_summary="유저의 이름 등록",
            operation_description="현재 접속한 유저의 이름을 등록한다.",
            request_body=UserSetNameClientSerializer,
            responses={201: openapi.Response(
                description="등록 성공",
                schema=UserSetNameServerSerializer()
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        name = request.data.get('name')
        if not name:
            return Response({"message": "이름을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

        user.name = name
        user.save()

        return Response({"message": "이름이 설정되었습니다."}, status=status.HTTP_201_CREATED)
    
class UserSetEnrollYearView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['유저 정보'],
            operation_summary="유저의 입학년도 등록",
            operation_description="현재 접속한 유저의 입학년도를 등록한다.",
            request_body=UserSetEnrollYearClientSerializer,
            responses={201: openapi.Response(
                description="등록 성공",
                schema=UserSetEnrollYearServerSerializer()
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        enrollYear = request.data.get('enrollYear')
        if not enrollYear:
            return Response({"message": "입학년도를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif enrollYear <= 1900 or enrollYear >= 2025:
            return Response({"message": "입학년도는 1900년 이상, 2025년 이하로만 가능합니다."}, status=status.HTTP_404_NOT_FOUND)

        user.enrollYear = enrollYear
        user.save()

        return Response({"message": "입학년도가 설정되었습니다."}, status=status.HTTP_201_CREATED)
    
class UserSetSchoolView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['유저 정보'],
            operation_summary="유저의 학교 등록",
            operation_description="현재 접속한 유저의 학교 정보를 등록한다.",
            request_body=UserSetSchoolClientSerializer,
            responses={201: openapi.Response(
                description="등록 성공",
                schema=UserSetSchoolServerSerializer()
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        schoolId = request.data.get('schoolId')
        if not schoolId:
            return Response({"message": "학교 id를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            theSchool = School.objects.get(pk=schoolId)
        except School.DoesNotExist:
            return Response({"message": "존재하지 않는 학교 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        user.school = theSchool
        user.save()

        return Response({"message": "학교 정보가 설정되었습니다."}, status=status.HTTP_201_CREATED)
        
class UserSetClassView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['유저 정보'],
            operation_summary="유저의 반 등록",
            operation_description="현재 접속한 유저의 반 정보를 등록한다.",
            request_body=UserSetClassClientSerializer,
            responses={201: openapi.Response(
                description="등록 성공",
                schema=UserSetClassServerSerializer()
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        school = user.school

        grade = request.data.get('grade')
        if not grade:
            return Response({"message": "학년을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif grade < 1 or grade > 6:
            return Response({"message": "학년은 1부터 6까지만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

        order = request.data.get('order')
        if not order:
            return Response({"message": "반을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif order < 1 or order > 10:
            return Response({"message": "반은 1부터 10까지만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        newClass = Class.objects.create(
            school = school,
            user = user,
            grade = grade,
            order = order,
            isAnonymous = True
        )
        returnSerializer = UserSetClassServerSerializer(newClass)
        return Response(returnSerializer.data, status=status.HTTP_201_CREATED)
    
class UserGetInfoView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['유저 정보'],
            operation_summary="유저의 정보 조회",
            operation_description="현재 접속한 유저의 정보(유저id, 아이디, 이름, 입학년도, 학교, 반)를 출력한다.",
            responses={201: openapi.Response(
                description="등록 성공",
                schema=UserGetInfoSerializer
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserGetInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)