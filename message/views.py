from .serializers import *
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
class SendMessageAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['쪽지'],
            operation_summary="쪽지 발송",
            operation_description="누군가(receiver)에게 쪽지를 발송한다.",
            request_body=SendMessageClientSerializer,
            responses={201: openapi.Response(
                description="발송 성공",
                schema=SendMessageServerSerializer
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        sender = request.user
        receiverId = request.data.get('receiverId')
        content = request.data.get('content')

        try:
            receiver = CustomUser.objects.get(pk=receiverId)
        except CustomUser.DoesNotExist:
            return Response({"error": "존재하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if sender == receiver:
            return Response({"error": "자신에게는 쪽지를 보낼 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        newMessage = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )
        responseSerializer = SendMessageServerSerializer(newMessage)

        return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        

class GetMessageAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['쪽지'],
            operation_summary="쪽지 조회",
            operation_description="나와 누군가(other) 사이에 나눴던 쪽지를 모두 조회한다.",
            responses={200: openapi.Response(
                description="조회 성공",
                schema=GetMessageServerSerializer
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request, otherId):
        user = request.user

        try:
            other = CustomUser.objects.get(pk=otherId)
        except CustomUser.DoesNotExist:
            return Response({"error": "존재하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user == other:
            return Response({"error": "자신과의 쪽지는 불러올 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        messageList = Message.objects.filter(Q(sender=user, receiver=other) | Q(sender=other, receiver=user))
        serializer = GetMessageServerSerializer(messageList, many=True, context={'user': user})

        return Response(serializer.data, status=status.HTTP_200_OK)