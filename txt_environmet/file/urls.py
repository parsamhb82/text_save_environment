from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', UploadFile.as_view()),
    path('files-list/', FilesView.as_view()),
    path('file-download/<int:pk>/', RetriveFile.as_view()),
    path('file-update/<int:pk>/', UpdateFile.as_view()),
    path('file-view/<int:pk>/', RetriveFileView.as_view()),
    path('file-delete/<int:pk>/', DeleteFileView.as_view()),
    path('update-content/<int:pk>/', UpdateContentView.as_view()),
    
]