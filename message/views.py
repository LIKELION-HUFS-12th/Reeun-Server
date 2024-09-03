from .serializers import *
from member.models import CustomUser
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

        newMessage = Message.objects.create(
            userOne=sender,
            userTwo=receiver,
            content=content
        )
        responseSerializer = SendMessageServerSerializer(newMessage)

        return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        