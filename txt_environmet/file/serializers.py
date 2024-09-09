from rest_framework import serializers
from .models import UploadedFile

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFile
        fields = '__all__'

class UpdateCreatFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['title', 'content']

class UploadFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UploadedFile
        fields = ['id', 'title', 'file']