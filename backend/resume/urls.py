from django.urls import path
from .views import (
    ResumeUploadView,
 
    ResumeOnlyATSView,
    ResumeJdATSView,
)

urlpatterns = [
    path("upload-resume/", ResumeUploadView.as_view()),
        path("resume/<uuid:resume_id>/ats/resume/", ResumeOnlyATSView.as_view()),
    path("resume/<uuid:resume_id>/ats/jd/", ResumeJdATSView.as_view()),
    
   
]
