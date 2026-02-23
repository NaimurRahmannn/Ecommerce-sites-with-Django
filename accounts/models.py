from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.models import Basemodel
# Create your models here.
class Profile(Basemodel):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100, null=True, blank=True)
    profile_image=models.ImageField(upload_to="profile")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email_token=str(uuid.uuid4()))
    
