from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ResumeListCreateView, ResumeDetailView, BlogListCreateView, BlogDetailView, BlogByCategoryView, BlogPostListView
from uuid import UUID

urlpatterns = [
    path('resumes/', ResumeListCreateView.as_view(), name='resume-list-create'),
    path('resumes/<uuid:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blog-post/<uuid:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/category/', BlogByCategoryView.as_view(), name='blog-by-category'),
    path('blog-posts/', BlogPostListView.as_view(), name='blog-posts'),
]

# # Serve media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)