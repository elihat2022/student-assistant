import secrets

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.shortcuts import reverse


# class Organization(models.Model):
#     name = models.CharField(max_length=100)
#     token = models.CharField(max_length=32, unique=True)

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.token:
#             self.token = secrets.token_hex(16)  # Genera un token aleatorio si no existe
#         super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("account:login")
