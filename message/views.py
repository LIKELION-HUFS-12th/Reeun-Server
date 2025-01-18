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
from member.serializers import GetNameSerializer

# Create your views here.
class GetMemberAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['쪽지'],
            operation_summary="쪽지를 하고 있는 유저 목록 조회",
            operation_description="쪽지를 나누고 있는 유저들의 정보를 조회한다\n\n(상대방이 이름을 설정해두지 않았을 경우 상대방의 name이 null로 표기됨)",
            responses={200: openapi.Response(
                description="조회 성공",
                schema=GetNameSerializer(many=True)
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request):
        user = request.user
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
        
        memberList = list()
        idList = set()
        for message in messages:
            if (message.sender == user):
                if (message.receiver.id not in idList):
                    idList.add(message.receiver.id)
                    memberList.append(message.receiver)
            else:
                if (message.sender.id not in idList):
                    idList.add(message.sender.id)
                    memberList.append(message.sender)
        print(memberList)
        
        serializer = GetNameSerializer(instance=memberList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            return Response({"statusCode": 404,
                             "message": "존재하지 않는 유저입니다."}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            return Response({"statusCode": 400,
                             "message": "자신에게는 쪽지를 보낼 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

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
                schema=GetMessageServerSerializer(many=True)
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request, otherId):
        user = request.user

        try:
            other = CustomUser.objects.get(pk=otherId)
        except CustomUser.DoesNotExist:
            return Response({"statusCode": 400,
                             "message": "존재하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user == other:
            return Response({"statusCode": 400,
                             "message": "자신과의 쪽지는 불러올 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        messageList = Message.objects.filter(Q(sender=user, receiver=other) | Q(sender=other, receiver=user))
        serializer = GetMessageServerSerializer(messageList, many=True, context={'user': user})

        return Response(serializer.data, status=status.HTTP_200_OK)