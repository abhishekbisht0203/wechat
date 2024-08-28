from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat (models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    chat = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.chat[:50]
    
    