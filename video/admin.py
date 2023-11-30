from django.contrib import admin

# Register your models here.
from .models import Video, MediaCategory

admin.site.register(Video)
admin.site.register(MediaCategory)
