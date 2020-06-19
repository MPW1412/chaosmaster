from rest_framework import serializers
from .models import StoredObjects, Images

class ImagesSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Images
        fields = ['id', 'uuid', 'image_url', 'order']

    def get_image_url(self,obj):
        request = self.context.get('request')
        if obj.path:
            image_url = obj.path.url
            return request.build_absolute_uri(image_url)

class CreateImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'uuid', 'path', 'order']
                
class StoredObjectsSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True)

    class Meta:
        model = StoredObjects
        fields = '__all__'

class CreateStoredObjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoredObjects
        fields = ["uuid","name", "owningEntity", "visibility", "locationEntityUUID","quantity",
                    "nestable","type","category","purpose","description","completed",
                    "standarisedObject"]


