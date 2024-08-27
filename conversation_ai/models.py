from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings


class Prompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False)
    prompt = models.CharField(max_length=512, null=False)
    response = models.CharField(max_length=1024,null=False)
    
    def save(self, *args, **kwargs):
        # Set the username field based on the related user object
        self.username = self.user.username
        super(Prompt, self).save(*args, **kwargs)