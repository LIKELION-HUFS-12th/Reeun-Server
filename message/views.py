from .serializers import *
from member.models import CustomUser
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

# Create your views here.
class SendMessageAPI(APIView):
    authentication_classes = [JWTAuthentication]

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

    def get(self, request):
        user = request.user
        otherId = request.data.get('otherId')

        try:
            other = CustomUser.objects.get(pk=otherId)
        except CustomUser.DoesNotExist:
            return Response({"error": "존재하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user == other:
            return Response({"error": "자신과의 쪽지는 불러올 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        messageList = Message.objects.filter(Q(sender=user, receiver=other) | Q(sender=other, receiver=user))
        serializer = GetMessageServerSerializer(messageList, many=True, context={'user': user})

        return Response(serializer.data, status=status.HTTP_200_OK)