from typing import cast
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,CommentSerializer, BlogSerializer, CategorySerializer,TagSerializer
from .models import Blog, Comment, Category, Tag
from app.ai_utils import generate_tags_for_blog
from django.db.models import Count, Q

# Create your views here.

class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User registered successfully"},
                    status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "related"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action in ["list", "retrieve", "related"]:
            return Blog.objects.filter(is_published=True).order_by("-created_at")

        return Blog.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        blog = cast(Blog, serializer.save(user=self.request.user))

        tag_names = generate_tags_for_blog(title=blog.title, content=blog.content)

        for tag_name in tag_names:
            tag_name = tag_name.strip().lower()

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)

    def update(self, request, *args, **kwargs):
        blog = self.get_object()

        if blog.user != request.user:
            return Response(
                {"error": "You can only update your own blog"},
                status=status.HTTP_403_FORBIDDEN,
            )

        partial = kwargs.pop("partial", True)
        serializer = self.get_serializer(blog, data=request.data, partial=partial)

        if serializer.is_valid():
            blog = cast(Blog, serializer.save())

            tag_names = generate_tags_for_blog(title=blog.title, content=blog.content)

            blog.tags.clear()

            for tag_name in tag_names:
                tag_name = tag_name.strip().lower()

                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    blog.tags.add(tag)

            response_serializer = self.get_serializer(blog)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()

        if blog.user != request.user:
            return Response(
                {"error": "You can only delete your own blog"},
                status=status.HTTP_403_FORBIDDEN,
            )

        blog.delete()
        return Response({"message": "Blog deleted successfully"})

    def retrieve(self, request, *args, **kwargs):
        blog = self.get_object()

        tag_ids = blog.tags.values_list("id", flat=True)

        related_blogs = (
            Blog.objects.filter(category=blog.category, is_published=True)
            .exclude(id=blog.pk)
            .annotate(matching_tags=Count("tags", filter=Q(tags__in=tag_ids)))
            .order_by("-matching_tags", "-created_at")[:5]
        )

        blog_serializer = self.get_serializer(blog)
        related_serializer = self.get_serializer(related_blogs, many=True)

        return Response(
            {
                "blog": blog_serializer.data,
                "related_blogs": related_serializer.data,
            }
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["list"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        blog_id = self.kwargs.get("blog_pk")

        if blog_id:
            return Comment.objects.filter(blog_id=blog_id).order_by("-id")

        return Comment.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        blog_id = self.kwargs.get("blog_pk")

        try:
            blog = Blog.objects.get(id=blog_id, is_published=True)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.user != request.user:
            return Response(
                {"error": "You can only delete your own comment"},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()
        return Response({"message": "Comment deleted successfully"})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
