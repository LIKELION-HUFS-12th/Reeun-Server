from rest_framework import serializers
from .models import Message
from member.serializers import GetNameSerializer

class SendMessageClientSerializer(serializers.ModelSerializer):
    receiverId = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['receiverId', 'content']

class SendMessageServerSerializer(serializers.ModelSerializer):
    sender = GetNameSerializer()
    receiver = GetNameSerializer()
    createDate = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'createDate']

class GetMessageServerSerializer(serializers.ModelSerializer):
    sender = GetNameSerializer()
    receiver = GetNameSerializer()
    createDate = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    isMyChat = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'createDate', 'isMyChat']

    def get_isMyChat(self, obj):
        currentUser = self.context['user']
        return obj.sender == currentUser
    
class ExitMessageClientSerializer(serializers.Serializer):
    otherId = serializers.IntegerField()