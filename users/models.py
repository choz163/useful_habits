from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    chat_id = models.CharField(max_length=64, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
