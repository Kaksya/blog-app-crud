from typing import cast
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,CommentSerializer, BlogSerializer, CategorySerializer,TagSerializer
from .models import Blog, Comment, Category, Tag
from app.ai_utils import generate_tags_for_blog
from django.db.models import Count, Q

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
         {'message': 'User registered successfully'},
         status=status.HTTP_201_CREATED
      )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_blogs(request):
    blogs = Blog.objects.filter(is_published=True)
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_blog_detail(request, blog_id):

    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    tag_ids = blog.tags.values_list("id", flat=True)

    related_blogs = (
        Blog.objects.filter(category=blog.category, is_published=True)
        .exclude(id=blog.pk)
        .annotate(matching_tags=Count("tags", filter=Q(tags__in=tag_ids)))
        .order_by("-matching_tags", "-created_at")[:5]
    )

    blog_serializer = BlogSerializer(blog)
    related_serializer = BlogSerializer(related_blogs, many=True)

    return Response(
        {"blog": blog_serializer.data, "related_blogs": related_serializer.data}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    serializer = BlogSerializer(data=request.data)

    if serializer.is_valid():
        blog = cast(Blog, serializer.save(user=request.user))

        tag_names = generate_tags_for_blog(title=blog.title, content=blog.content)

        print("GENERATED TAGS:", tag_names)

        for tag_name in tag_names:
            tag_name = tag_name.strip().lower()

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)

        response_serializer = BlogSerializer(blog)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    if blog.user != request.user:
        return Response(
            {"error": "You can only update your own blog"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = BlogSerializer(blog, data=request.data, partial=True)

    if serializer.is_valid():
        blog = cast(Blog, serializer.save())

        tag_names = generate_tags_for_blog(title=blog.title, content=blog.content)

        blog.tags.clear()

        for tag_name in tag_names:
            tag_name = tag_name.strip().lower()

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)

        response_serializer = BlogSerializer(blog)

        return Response(response_serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    if blog.user != request.user:
        return Response(
            {"error": "You can only delete your own blog"},
            status=status.HTTP_403_FORBIDDEN,
        )

    blog.delete()
    return Response({"message": "Blog deleted successfully"})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_comments(request, blog_id):
    comments = Comment.objects.filter(blog_id=blog_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id, is_published=True)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user, blog=blog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if comment.user != request.user:
        return Response(
            {"error": "You can only delete your own comment"},
            status=status.HTTP_403_FORBIDDEN,
        )

    comment.delete()
    return Response({"message": "Comment deleted successfully"})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_tags(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)
