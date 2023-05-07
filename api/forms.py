from django import forms
from .models import Blogs

class BlogForm(forms.ModelForm): #ModelForm for the Blogs model
    class Meta:
        model = Blogs #model to be used
        fields = ('title', 'content', 'image') #fields that will be returned in the response