from django import forms
from django.forms import TextInput

from .models import Video

class VideoForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Video
        fields = [
            'caption', 'media_category', 'keywords', 'createdby', 'video', 
        ]
        widgets = {
            'caption': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%',
                'placeholder': 'Title'
                }),    
            'keywords': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 100%;',
                'placeholder': 'Enter keywords'
                })},


