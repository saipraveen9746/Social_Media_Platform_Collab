from django.db import models
from Account.models import CustomUser

# Create your models here.
class Story(models.Model):
    author = models.ForeignKey(CustomUser, related_name='story', on_delete=models.CASCADE)
    caption = models.TextField(null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    

    def __str__(self):
        return f"story by {self.author.username} at {self.created_at} :id:{self.id}"
    