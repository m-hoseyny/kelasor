from django.db import models
from django.utils import timezone
from TelegramAdmin.models import User
# Create your models here.


class File(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    file_id = models.TextField(unique=True)
    mime_type = models.CharField(max_length=100)
    file_size = models.IntegerField()
    file_name = models.CharField(max_length=1000)
    file_description = models.CharField(max_length=1025, null=True)
    search_field = models.TextField(default='')
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'files'
        ordering = ['-download_count', '-created_at']
