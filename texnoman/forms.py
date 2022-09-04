from django import forms
from .models import Blog,Comment

class UpdateBlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=['title','content','image','category']
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']