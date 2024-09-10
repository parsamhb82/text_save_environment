from rest_framework import serializers
from .models import UploadedFile

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFile
        fields = '__all__'


class UploadFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UploadedFile
        fields = ['title', 'file']