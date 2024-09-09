from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'
        
class UpdateCreatFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('title', 'content')