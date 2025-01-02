from django.db import models

# Create your models here.
class Chats(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    data = models.TextField(default=list())
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)