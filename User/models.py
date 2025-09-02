from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    position = models.CharField(max_length=100, null=True, blank=True)
    #contact_number = models.CharField(max_length=100, null=True, blank=True)
    #branch_code = models.CharField(max_length=10, null=True, blank=True)