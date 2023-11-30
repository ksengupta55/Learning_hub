from django import forms
from django.forms import TextInput

from .models import Lesson, Category

class LessonForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Lesson
        fields = [
            'title', 'category', 'keywords', 'createdby', 'problem_document', 'answer_document', 
        ]
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%',
                'placeholder': 'Title'
                }),    
            'keywords': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 100%;',
                'placeholder': 'Enter keywords'
                })}

'''class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()'''   

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['category',]
        validate = False




        
        
          


