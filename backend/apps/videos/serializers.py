from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Video
        fields = "__all__"

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/api/videos/{obj.id}/file/")
