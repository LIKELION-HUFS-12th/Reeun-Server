from django.db import models
from django.conf import settings

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sentMessage")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receivedMessage")
    content = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)