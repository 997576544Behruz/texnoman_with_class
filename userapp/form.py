from texnoman.models import Blog
from django import forms
class AddBlogForm(forms.ModelForm):
    tags=forms.CharField(max_length=500)
    class Meta:
        model=Blog
        fields=['title','content','image','category']