from django.db import models
from django.conf import settings

# Create your models here.
class Message(models.Model):
    userOne = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userTwo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)