from django.urls import path

from .views import (
    analyze_resume_view,
    chatbot_view,
)

urlpatterns = [
    path(
        "analyze/", analyze_resume_view,),
    path(
        "chat/",chatbot_view,),
]