from rest_framework import serializers
from .models import Message
from member.serializers import GetNicknameSerializer

class SendMessageClientSerializer(serializers.ModelSerializer):
    receiverId = serializers.IntegerField

    class Meta:
        model = Message
        fields = ['receiverId', 'content']

class SendMessageServerSerializer(serializers.ModelSerializer):
    sender = GetNicknameSerializer()
    receiver = GetNicknameSerializer()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content']

class GetMessageClientSerializer(serializers.Serializer):
    otherId = serializers.IntegerField()

class GetMessageServerSerializer(serializers.ModelSerializer):
    sender = GetNicknameSerializer()
    receiver = GetNicknameSerializer()
    isMyChat = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'isMyChat']

    def get_isMyChat(self, obj):
        currentUser = self.context['user']
        return obj.sender == currentUser