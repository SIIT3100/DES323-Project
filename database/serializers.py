from rest_framework import serializers

class AuthenticationAPISerializer(serializers.Serializer):

    username = serializers.CharField(required=False, max_length=255)
    password = serializers.CharField(required=False)
    row = serializers.CharField(required=False)