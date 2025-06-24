from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from .models import Resume, Blog
from .serializers import (
    UserSerializer,
    ResumeSerializer,
    BlogSerializer,
    BlogPostSerializer
)

User = get_user_model()

class APIRootView(APIView):
    """
    API Root endpoint - provides information about available endpoints
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Welcome to Portfolio Backend API",
            "version": "1.0.0",
            "status": "online",
            "endpoints": {
                "health": "/api/health/",
                "resumes": "/api/resumes/",
                "resume_detail": "/api/resumes/{id}/",
                "blogs": "/api/blogs/",
                "blog_detail": "/api/blog-post/{id}/",
                "blog_posts": "/api/blog-posts/",
                "auth": {
                    "register": "/api/user/register/",
                    "token": "/api/token/",
                    "refresh": "/api/token/refresh/"
                },
                "admin": "/admin/"
            },
            "database": "MongoDB" if hasattr(request, '_mongodb_connected') else "Connected",
            "media_storage": "Cloudinary"
        }, status=status.HTTP_200_OK)

class HealthCheckView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access the health check endpoint

    def get(self, request, *args, **kwargs):
        return Response({
            "status": "healthy",
            "message": "Server is up and running"
        }, status=status.HTTP_200_OK)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)


class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)


class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self):
        return get_object_or_404(Resume, user_id=self.kwargs["pk"])

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "data": "Resume deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all().order_by("-created_at")
    serializer_class = BlogSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({
            "status": status.HTTP_201_CREATED,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "data": "Blog deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class BlogByCategoryView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category:
            return Blog.objects.filter(category__iexact=category)
        return Blog.objects.none()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)


class BlogPostListView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by("-created_at")
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": response.status_code,
            "data": response.data
        }, status=response.status_code)
