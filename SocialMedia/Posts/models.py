from django.db import models
from Account.models import CustomUser
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    liked_by = models.ManyToManyField(CustomUser, related_name='liked_posts', through='Like')

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
    
    
    
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        
        
    def __str__(self):
        return f"liked by {self.user.username} at {self.post}"
    
    
    
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment was created

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"