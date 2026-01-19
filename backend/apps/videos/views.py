from rest_framework import viewsets, permissions, views
from .models import Video
from .serializers import VideoSerializer
from .permissions import IsCreatorOrAdmin, IsOwnerOrReadOnly
from django.http import FileResponse, Http404

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsCreatorOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly, IsCreatorOrAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [p() for p in permission_classes]

    def query_set(self):
        user = self.request.user

        if not user.is_authenticated:
            return Video.objects.filter(is_public=True)

        if user.role == "ADMIN":
            return Video.objects.all()

        if user.role == "CREATOR":
            return Video.objects.filter(owner=user)

        return Video.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class VideoFileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise Http404

        if not video.is_public:
            if request.user != video.owner and request.user.role != "ADMIN":
                raise Http404

        return FileResponse(
            video.file.open(mode='rb'), 
            as_attachment=False, 
            filename=video.file.name
        )
