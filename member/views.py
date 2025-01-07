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

    @swagger_auto_schema(
        tags=['member'],
        operation_summary="회원가입",
        operation_description="회원가입 한다.",
        request_body=CustomRegisterSerializer,
        responses={201: openapi.Response(
            description="회원가입 성공",
            schema=RegisterResponseSerializer()
        )})
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
        return Response({"statusCode": 400,
                          "message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({"statusCode": 400,
                        "message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 허용

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")
        if user.check_password(password):
            user.delete()  # 비밀번호 확인 후 사용자 삭제
            return Response({"detail": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"statusCode": 400,
                             "message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
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
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        name = request.data.get('name')
        if not name:
            return Response({"statusCode": 400,
                             "message": "이름을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        enrollYear = request.data.get('enrollYear')
        if not enrollYear:
            return Response({"statusCode": 400,
                             "message": "입학년도를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif enrollYear <= 1900 or enrollYear >= 2025:
            return Response({"statusCode": 400,
                             "message": "입학년도는 1900년 이상, 2025년 이하로만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        schoolId = request.data.get('schoolId')
        if not schoolId:
            return Response({"statusCode": 400,
                             "message": "학교 id를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            theSchool = School.objects.get(pk=schoolId)
        except School.DoesNotExist:
            return Response({"statusCode": 404,
                             "message": "존재하지 않는 학교 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
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
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        school = user.school

        grade = request.data.get('grade')
        if not grade:
            return Response({"statusCode": 400,
                             "message": "학년을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif grade < 1 or grade > 6:
            return Response({"statusCode": 400,
                             "message": "학년은 1부터 6까지만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

        order = request.data.get('order')
        if not order:
            return Response({"statusCode": 400,
                             "message": "반을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif order < 1 or order > 10:
            return Response({"statusCode": 400,
                             "message": "반은 1부터 10까지만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        theClass = Class.objects.filter(user=user, grade=grade).first()
        if theClass is not None:
            theClass.delete()
        
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
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserGetInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OpenNicknameSchoolView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['유저 목록 조회 관련'],
        operation_summary="자신의 이름을 학교에게 공개",
        operation_description="현재 접속한 유저의 이름을 앞으로 학교 멤버들에게 공개한다. (공개 시 비공개 전환 불가능)",
        responses={201: openapi.Response(
            description="공개 성공",
        )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.school is None:
            return Response({"statusCode": 404,
                              "message": "학교 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if user.isAnonymousSchool == False:
            return Response({"statusCode": 400,
                              "message": "이미 이름이 학교에 공개가 되어 있습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        user.isAnonymousSchool = False
        user.save()
        return Response({"message": "앞으로 이름이 자신의 학교 멤버들에게 공개됩니다."}, status=status.HTTP_201_CREATED)
    

class OpenNicknameClassView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['유저 목록 조회 관련'],
        operation_summary="자신의 이름을 학급에게 공개",
        operation_description="현재 접속한 유저의 이름을 앞으로 자신의 특정 학년(grade)의 학급 멤버들에게 공개한다. (공개 시 비공개 전환 불가능)",
        request_body=UserOpenNicknameClassClientSerializer(),
        responses={201: openapi.Response(
            description="공개 성공",
        )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.school is None:
            return Response({"statusCode": 404,
                              "message": "학교 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        grade = request.data.get('grade')
        if not grade:
            return Response({"statusCode": 400,
                              "message": "'grade' 값이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        theClass = Class.objects.get(user=user, grade=grade)
        if theClass.isAnonymous == False:
            return Response({"statusCode": 400,
                              "message": "이미 이름이 학급에 공개가 되어 있습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        theClass.isAnonymous = False
        theClass.save()
        return Response({"message": "앞으로 이름이 자신의 학급 멤버들에게 공개됩니다."}, status=status.HTTP_201_CREATED)



class UserGetSchoolMemberView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['유저 목록 조회 관련'],
        operation_summary="같은 학교 유저 목록 조회",
        operation_description="현재 접속한 유저의 학교와 동일한 학교의 유저 중, 정보 공개를 해 둔 사람들을 모두 가져온다.",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=GetNameSerializer(many=True)
        )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self,request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.school is None:
            return Response({"statusCode": 404,
                              "message": "학교 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        school = user.school

        if user.isAnonymousSchool == True:
            return Response({"statusCode": 400,
                              "message": "자신의 이름을 먼저 공개해야 다른 유저의 목록을 조회할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        usersInSchool = User.objects.filter(school=school, isAnonymousSchool=False)
        serializer = GetNameSerializer(usersInSchool, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserGetClassMemberView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['유저 목록 조회 관련'],
        operation_summary="같은 학교의 특정 학년의 학급 유저 목록 조회",
        operation_description="현재 접속한 유저의 학교와 동일한 학교의 특정 학년(grade)의 특정 학급(oredr)에서, 정보 공개를 해 둔 사람들을 모두 가져온다.",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=GetNameSerializer(many=True)
        )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self,request, grade):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"statusCode": 404,
                             "message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.school is None:
            return Response({"statusCode": 404,
                              "message": "학교 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        school = user.school

        myClass = Class.objects.get(user=user, grade=grade)
        if myClass is None:
            return Response({"statusCode": 404,
                              "message": "학급 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        if myClass.isAnonymous == True:
            return Response({"statusCode": 400,
                              "message": "자신의 이름을 먼저 공개해야 다른 유저의 목록을 조회할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        userClass = Class.objects.filter(school=myClass.school, grade=myClass.grade, order=myClass.order, isAnonymous=False)
        usersInClass = []
        for cls in userClass:
            usersInClass.append(cls.user)

        serializer = GetNameSerializer(usersInClass, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

