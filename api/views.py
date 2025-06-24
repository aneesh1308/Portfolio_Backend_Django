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
                "admin": "/admin/",
                "setup": "/api/setup-admin/",
                "clear_database": "/api/clear-database/"
            },
            "database": "MongoDB" if hasattr(request, '_mongodb_connected') else "Connected",
            "media_storage": "Cloudinary"
        }, status=status.HTTP_200_OK)


class SetupAdminView(APIView):
    """
    Setup admin user - clears existing data and creates fresh admin user and resume
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            email = 'araneesh08@gmail.com'
            password = 'Anee&H08'

            # Check database connection
            from django.db import connection
            db_info = {
                "engine": connection.settings_dict.get('ENGINE', 'Unknown'),
                "name": connection.settings_dict.get('NAME', 'Unknown')
            }

            # Clear existing data for this email
            try:
                existing_user = User.objects.get(email=email)
                # Delete associated resumes
                Resume.objects.filter(user=existing_user).delete()
                # Delete user
                existing_user.delete()
                print("Cleared existing admin user and data")
            except User.DoesNotExist:
                pass
            except Exception as db_error:
                return Response({
                    "success": False,
                    "error": f"Database error: {str(db_error)}",
                    "database_info": db_info,
                    "suggestion": "Please add DATABASE_URL environment variable with PostgreSQL connection string"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Create fresh admin user
            user = User.objects.create_user(
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()

            # Create fresh resume
            resume = Resume.objects.create(
                user=user,
                email=email,
                name='Araneesh Portfolio',
                title='Full Stack Developer',
                bio='Experienced developer with expertise in web technologies.',
                phone_number='+1234567890',
                location='Remote'
            )

            # Test authentication
            from django.contrib.auth import authenticate
            auth_user = authenticate(email=email, password=password)
            auth_status = "SUCCESS" if auth_user else "FAILED"

            return Response({
                "success": True,
                "message": "Admin setup completed successfully! Fresh data created.",
                "data": {
                    "admin_user": {
                        "email": user.email,
                        "password": password,
                        "user_id": str(user.id),
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser,
                        "is_active": user.is_active,
                        "auth_test": auth_status
                    },
                    "resume": {
                        "resume_id": str(resume.user_id),
                        "name": resume.name,
                        "title": resume.title,
                        "email": resume.email
                    },
                    "database_info": {
                        "total_users": User.objects.count(),
                        "total_resumes": Resume.objects.count(),
                        "database_engine": db_info["engine"],
                        "database_name": db_info["name"]
                    }
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            return Response({
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "database_info": db_info if 'db_info' in locals() else "Unknown"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClearDatabaseView(APIView):
    """
    Clear all data from database - use with caution!
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Clear all data
            from .models import Blog
            
            blog_count = Blog.objects.count()
            resume_count = Resume.objects.count()
            user_count = User.objects.count()
            
            # Delete all records
            Blog.objects.all().delete()
            Resume.objects.all().delete()
            User.objects.all().delete()

            return Response({
                "success": True,
                "message": "Database cleared successfully!",
                "deleted": {
                    "blogs": blog_count,
                    "resumes": resume_count,
                    "users": user_count
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            return Response({
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
