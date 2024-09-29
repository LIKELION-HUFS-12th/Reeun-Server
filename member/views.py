# community/member/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .serializers import CustomRegisterSerializer, CustomUserDetailSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from dj_rest_auth.views import LoginView

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
                    "username": user.username,
                    "nickname": user.nickname,
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
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        name = request.data.get('name')
        if not name:
            return Response({"detail": "이름을 입력해 주세요."}, status=status.HTTP_404_NOT_FOUND)

        user.name = name
        user.save()

        return Response({"detail": "이름이 설정되었습니다."}, status=status.HTTP_201_CREATED)
    
class UserSetEnrollYearView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        enrollYear = request.data.get('enrollYear')
        if not enrollYear:
            return Response({"detail": "입학년도를 입력해 주세요."}, status=status.HTTP_404_NOT_FOUND)
        elif enrollYear <= 1900 or enrollYear >= 2025:
            return Response({"detail": "입학년도는 1900년 이상, 2025년 이하로만 가능합니다."}, status=status.HTTP_404_NOT_FOUND)

        user.enrollYear = enrollYear
        user.save()

        return Response({"detail": "입학년도가 설정되었습니다."}, status=status.HTTP_201_CREATED)

# 유저 정보 조회 및 생성
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 허용

    def get(self, request):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = CustomUserDetailSerializer(user)

        data = user_serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # if UserProfile.objects.filter(user=request.user).exists():
        #     return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # serializer = UserProfileSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save(user=request.user)  # 사용자와 관련된 프로필 생성
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("serializer.errors", status=status.HTTP_400_BAD_REQUEST)

# 반 정보 조회 및 수정
class GradeView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 허용

    # def get(self, request):
    #     try:
    #         profile = UserProfile.objects.get(user=request.user)
    #         serializer = GradeSerializer(profile)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except UserProfile.DoesNotExist:
    #         return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    # def put(self, request):
    #     try:
    #         profile = UserProfile.objects.get(user=request.user)
    #     except UserProfile.DoesNotExist:
    #         return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = GradeSerializer(profile, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)