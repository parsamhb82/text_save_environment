from django.contrib import admin
from .models import UploadedFile
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'updated_at')
