from django.db import models
from django.conf import settings

# Create your models here.
class Claim(models.Model):
    claimingUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="myClaim")
    claimedUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receivedClaim")
    reason = models.TextField()