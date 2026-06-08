from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path,include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet,BlogViewSet,CommentViewSet,CategoryViewSet, TagViewSet

router = DefaultRouter()

router.register("register", RegisterViewSet, basename="register")
router.register("blogs", BlogViewSet, basename="blogs")
router.register("categories", CategoryViewSet, basename="categories")
router.register("tags", TagViewSet, basename="tags")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "blogs/<int:blog_pk>/comments/",
        CommentViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="blog-comments",
    ),
    path(
        "comments/<int:pk>/",
        CommentViewSet.as_view(
            {
                "delete": "destroy",
            }
        ),
        name="comment-delete",
    ),
]
