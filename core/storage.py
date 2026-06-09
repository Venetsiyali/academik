import os
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.core.files.base import ContentFile
import mimetypes
from django.urls import reverse

@deconstructible
class DatabaseStorage(Storage):
    """
    Custom Django Storage backend that saves files to the PostgreSQL database 
    using the core.models.DBFile model.
    Useful for serverless environments (like Vercel) where the filesystem is read-only.
    """

    def _save(self, name, content):
        from core.models import DBFile
        
        # Determine content type
        content_type, _ = mimetypes.guess_type(name)
        if not content_type:
            content_type = 'application/octet-stream'

        # Read the file content
        content.seek(0)
        file_bytes = content.read()
        
        # Ensure unique name
        base_name, ext = os.path.splitext(name)
        counter = 1
        final_name = name
        while DBFile.objects.filter(file_name=final_name).exists():
            final_name = f"{base_name}_{counter}{ext}"
            counter += 1

        # Save to database
        DBFile.objects.create(
            file_name=final_name,
            content=file_bytes,
            content_type=content_type,
            size=len(file_bytes)
        )
        
        return final_name

    def _open(self, name, mode='rb'):
        from core.models import DBFile
        try:
            db_file = DBFile.objects.get(file_name=name)
            return ContentFile(db_file.content, name=db_file.file_name)
        except DBFile.DoesNotExist:
            return None

    def exists(self, name):
        from core.models import DBFile
        return DBFile.objects.filter(file_name=name).exists()

    def url(self, name):
        # Maps to the 'serve_db_file' view
        return f"/media-db/{name}"

    def size(self, name):
        from core.models import DBFile
        try:
            return DBFile.objects.get(file_name=name).size
        except DBFile.DoesNotExist:
            return 0
