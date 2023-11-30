from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MediaCategory(models.Model):
    class Meta:
        verbose_name_plural = "media categories"
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.name) 

class Video(models.Model):
    caption = models.CharField(max_length=200, unique=True)
    media_category = models.ForeignKey(MediaCategory, max_length=50, on_delete=models.CASCADE, null=True)
    keywords = models.CharField(max_length=200, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)    
    #media_file = models.FileField(upload_to = 'full_length', blank=False, null=True)
    video = models.FileField(upload_to="media", blank=False, null=True)

    def __str__(self):
        return self.caption