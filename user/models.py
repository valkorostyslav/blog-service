from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    auto_reply_enabled = models.BooleanField(default=False)
    auto_reply_delay = models.IntegerField(default=0)