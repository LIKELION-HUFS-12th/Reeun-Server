# community/member/views.py

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import CustomRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from dj_rest_auth.views import LoginView

User = get_user_model()

# 회원가입
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]


# 로그아웃
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 현재 인증된 사용자의 모든 RefreshToken을 블랙리스트에 추가하여 무효화
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 회원탈퇴
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")
        if user.check_password(password):
            user.delete()
            return Response({"detail": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)
