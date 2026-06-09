from django.db import models
import uuid

from django.conf import settings

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Notification(UUIDModel):
    TYPE_CHOICES = (
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('SUCCESS', 'Success'),
        ('ERROR', 'Error'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True, help_text="Link to the related object")
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='INFO')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient}: {self.message[:20]}"

class DBFile(UUIDModel):
    """
    Stores uploaded files (images, documents) directly in the database 
    to bypass Vercel's read-only filesystem.
    """
    file_name = models.CharField(max_length=500, unique=True, db_index=True)
    content = models.BinaryField()
    content_type = models.CharField(max_length=255, blank=True)
    size = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
