from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
