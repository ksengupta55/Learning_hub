from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.name)
    
    
class Lesson(models.Model):
    title = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, max_length=50, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=200, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    problem_statement = models.TextField(max_length=255, blank=True, null=True)
    problem_document = models.FileField(upload_to = "pdf", blank=False, null=True)
    answer_document = models.FileField(upload_to = "answer", blank=False, null=True)
    #problem_document = models.FileField(upload_to = 'static/pdf', blank=False)
    #answer_document = models.FileField(upload_to = 'static/pdf/answer', blank=False)
 
    def __str__(self):
        return str(self.id)
    
      
    

    
    
    

