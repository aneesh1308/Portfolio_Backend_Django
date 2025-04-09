from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Resume, Blog
from .serializers import UserSerializer, ResumeSerializer, BlogSerializer, BlogPostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self):
        return get_object_or_404(Resume, user_id=self.kwargs["pk"])
    
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all().order_by("-created_at")
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

class BlogByCategoryView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category:
            return Blog.objects.filter(category__iexact=category)
        return Blog.objects.none()
    
class BlogPostListView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by("-created_at")
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

