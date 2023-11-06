from rest_framework import serializers

class AuthenticationAPISerializer(serializers.Serializer):

    row = serializers.IntegerField(required=False)