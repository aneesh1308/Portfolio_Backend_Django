from django.urls import path
from .views import ResumeListCreateView, ResumeDetailView

urlpatterns = [
    path('resumes/', ResumeListCreateView.as_view(), name='resume-list-create'),
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
]