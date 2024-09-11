from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .models import UploadedFile
from .serializers import UploadFileSerializer, FileSerializer
import io
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuser
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse

class FilesView(ListAPIView):
    serializer_class = FileSerializer
    queryset  = UploadedFile.objects.all()
    permission_classes = [IsAuthenticated]
    
class UploadFile(CreateAPIView):
    serializer_class = UploadFileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            uploaded_file = serializer.validated_data.get('file')

            if uploaded_file:
                file_content = uploaded_file.read().decode('utf-8')

                serializer.save(user=self.request.user, content=file_content)
            else:
                return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetriveFile(RetrieveAPIView):
    serializer_class = FileSerializer
    queryset = UploadedFile.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        uploaded_file = self.get_object()
        if request.user != uploaded_file.user:
            return Response({'error': 'You are not authorized to view this file'}, status=status.HTTP_403_FORBIDDEN)
        return FileResponse(uploaded_file.file, as_attachment=True, filename=uploaded_file.title)

class UpdateFile(UpdateAPIView):
    serializer_class = UploadFileSerializer
    queryset = UploadedFile.objects.all()
    permission_classes = [IsAuthenticated]
    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            return Response({'error': 'You are not authorized to update this file'}, status=status.HTTP_403_FORBIDDEN)
        
    def perform_update(self, serializer):
        if serializer.is_valid():
            uploaded_file = serializer.validated_data.get('file')

            if uploaded_file:
                file_content = uploaded_file.read().decode('utf-8')

                serializer.save(user=User.objects.first(), content=file_content)
            else:
                return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetriveFileView(RetrieveAPIView):
    serializer_class = FileSerializer
    queryset = UploadedFile.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        uploaded_file = self.get_object()
        if request.user != uploaded_file.user:
            return Response({'error': 'You are not authorized to view this file'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)

from django.core.files.storage import default_storage
from rest_framework.exceptions import PermissionDenied
class DeleteFileView(DestroyAPIView):
    serializer_class = FileSerializer
    queryset = UploadedFile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied({'error': 'You are not authorized to delete this file'})
        return obj

    def perform_destroy(self, instance):
        # Delete the file from the file system if it exists
        if instance.file and default_storage.exists(instance.file.name):
            default_storage.delete(instance.file.name)
        
        super().perform_destroy(instance)

class ViewFiles(ListAPIView):
    serializer_class = FileSerializer
    queryset = UploadedFile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)

from .serializers import FileContentSerializer
from django.core.files.base import ContentFile
class UpdateContentView(UpdateAPIView):
    serializer_class = FileContentSerializer
    queryset = UploadedFile.objects.all()
    # permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     obj = super().get_object()
    #     if obj.user != self.request.user:
    #         return Response({'error': 'You are not authorized to update this file'}, status=status.HTTP_403_FORBIDDEN)
    
    def perform_update(self, serializer):
        # Get the instance of the file record
        instance = self.get_object()

        # Get the new content from the validated data
        new_content = serializer.validated_data.get('content', '')

        if new_content:
            # Update the instance.content with the new content
            instance.content = new_content
            
            # Delete the old file if it exists
            if instance.file and default_storage.exists(instance.file.name):
                default_storage.delete(instance.file.name)

            # Create a new file from the content
            new_file = ContentFile(new_content.encode('utf-8'))

            # Save the new content to the same file name (rewrite the file)
            instance.file.save(instance.file.name, new_file)
            instance.content = new_content
            instance.save()

        # Save the instance (with the updated content)
        serializer.save()
            


        
        
    

    

        