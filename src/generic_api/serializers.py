from rest_framework import serializers
from django.contrib import auth

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'author', 'created_at')
        read_only_field = ('created_at')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.get_user_model()
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        user = auth.get_user_model()
        return user.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, data):
        data_keys = data.keys()
        if 'username' not in data_keys or 'password' not in data_keys:
            raise serializers.ValidationError('ログイン情報が不足しています')
        return data
