from rest_framework import serializers
from django.contrib import auth
from django.urls import reverse

from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # get_変数名のメソッドを定義して、そこで値を受け取る
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'comment', 'author', 'created_at', 'detail_url')
        read_only_fields = ('id', 'post', 'author', 'created_at')

    def get_detail_url(self, obj):  # get_(serializers.SerializerMethodField()で定義した変数名)
        return reverse('comment_retrieve_destroy', kwargs={ 'post_id': obj.post_id, 'cmt_id': obj.id })  # URLの名前から逆引き


class PostSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)
    detail_url = serializers.SerializerMethodField()  # get_変数名のメソッドを定義して、そこで値を受け取る

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'created_at', 'comments', 'detail_url')
        read_only_fields = ('author', 'created_at')
    
    def get_detail_url(self, obj):  # get_(serializers.SerializerMethodField()で定義した変数名)
        return reverse('post_detail', kwargs={ 'id': obj.id })  # URLの名前から逆引き


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
