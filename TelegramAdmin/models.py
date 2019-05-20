from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    chat_type = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, default='start')
    premium_type = models.CharField(max_length=50, null=True)
    last_checked_bot = models.DateTimeField(default=timezone.now)
    user_rate = models.FloatField(default=0)
    credit = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users'


class UserSearch(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    query = models.TextField()
    response = models.CharField(max_length=20)
    search_result = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users_searches'
