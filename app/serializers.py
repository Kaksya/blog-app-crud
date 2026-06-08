from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Comment, Category, Tag

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
