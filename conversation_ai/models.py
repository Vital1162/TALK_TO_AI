from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=2024)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.response

class Prompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False)
    prompt = models.CharField(max_length=512, null=False)
    response = models.CharField(max_length=1024,null=False)
    timestamp = models.DateTimeField(null=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='prompts')


    def save(self, *args, **kwargs):
        # Set the username field based on the related user object
        self.username = self.user.username
        super(Prompt, self).save(*args, **kwargs)







