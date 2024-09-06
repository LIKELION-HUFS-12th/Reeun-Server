from .serializers import *
from .models import *
from member.models import CustomUser
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

# Create your views here.
class MakeClaimAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['신고'],
            operation_summary="신고하기",
            operation_description="누군가(object)를 신고한다.",
            request_body=MakeClaimClientSerializer,
            responses={201: openapi.Response(
                description="발송 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example="신고가 완료되었습니다.")
                    }
                )
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        claimingUser = request.user
        objectId = request.data.get('objectId')
        reason = request.data.get('reason')

        try:
            claimedUser = CustomUser.objects.get(pk=objectId)
        except CustomUser.DoesNotExist:
            return Response({"message": "존재하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if claimingUser == claimedUser:
            return Response({"message": "자기 자신은 신고할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        isExist = Claim.objects.filter(claimingUser=claimingUser, claimedUser=claimedUser).exists()
        if isExist:
            return Response({"message": "이미 신고한 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        newClaim = Claim.objects.create(
            claimingUser = claimingUser,
            claimedUser = claimedUser,
            reason = reason
        )

        # claimedUser의 신고 개수를 세어 탈퇴시킨다
        claimedUserClaimCount = claimedUser.receivedClaim.count()
        if claimedUserClaimCount >= 3:
            claimedUser.delete()

        return Response({"message": "신고가 완료되었습니다."}, status=status.HTTP_201_CREATED)
