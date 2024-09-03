from rest_framework import serializers
from .models import Message
from member.serializers import CustomUserDetailSerializer

class SendMessageClientSerializer(serializers.ModelSerializer):
    receiverId = serializers.IntegerField

    class Meta:
        model = Message
        fields = ['receiverId', 'content']

class SendMessageServerSerializer(serializers.ModelSerializer):
    sender = CustomUserDetailSerializer(source='userOne')
    receiver = CustomUserDetailSerializer(source='userTwo')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content']