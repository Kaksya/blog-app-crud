from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_user),
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("blogs/", views.get_blogs),
    path("blogs/create/", views.create_blog),
    path("blogs/<int:blog_id>/", views.get_blog_detail),
    path("blogs/<int:blog_id>/update/", views.update_blog),
    path("blogs/<int:blog_id>/delete/", views.delete_blog),
    path("blogs/<int:blog_id>/comments/", views.get_comments),
    path("blogs/<int:blog_id>/comments/create/", views.create_comment),
    path("comments/<int:comment_id>/delete/", views.delete_comment),
    path("categories/", views.get_categories),
    path("tags/", views.get_tags),
]
