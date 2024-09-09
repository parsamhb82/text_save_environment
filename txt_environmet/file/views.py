from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UploadedFile
from .serializers import UploadFileSerializer, UpdateCreatFileSerializer, FileSerializer
import io
from datetime import datetime
from django.contrib.auth.models import User

class FileUploadView(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('file')
        title = request.data.get('title', '')
        
        if file:
            file_content = file.read().decode('utf-8')
        else:
            file_content = ''
        
        # Create an instance of UploadedFile with the file content
        uploaded_file = UploadedFile(
            user = User.objects.get(id = 1),
            file=file,
            title=title,
            content=file_content,
            uploaded_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        uploaded_file.save()
        
        serializer = UploadFileSerializer(uploaded_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)