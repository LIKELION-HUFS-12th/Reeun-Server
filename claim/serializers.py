from rest_framework import serializers

class MakeClaimClientSerializer(serializers.Serializer):
    objectId = serializers.IntegerField()
    reason = serializers.CharField()