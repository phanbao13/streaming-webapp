from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, VideoFileView
from django.urls import path
router = DefaultRouter()
router.register("", VideoViewSet, basename='video')

urlpatterns = router.urls + [
        path("<int:pk>/file/", VideoFileView.as_view(), name="video-file"),
    ]
    