from django.db import models
from django.contrib.auth.models import User
from base.models import Basemodel
# Create your models here.
class Profile(Basemodel):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles")
    is_email_verified=models.BooleanField(False)
    email_token=models.CharField(max_length=100, null=True, blank=True)
    profile_image=models.ImageField(upload_to="profile")
    
