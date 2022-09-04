from django import views
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
# Create your models here.
class UserProfile(AbstractUser):
    image=models.ImageField(upload_to="users/%Y/%m/%d")
    bio = models.TextField(null=True,blank=True)
    birthday=models.DateField(null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    phone_number=models.CharField(max_length=15,null=True,blank=True)
    def __str__(self):
        return self.username
    @property
    def age(self):
        return date.today().year-self.birthday.year

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    image=models.ImageField(upload_to="Category/%Y/%m/%d")
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        return super().save(*args,**kwargs)

class Blog(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)
    content=models.TextField()
    image=models.ImageField(upload_to="blog/%Y/%m/%d")
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now_add=True)
    views=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    tags=models.ManyToManyField(Tag)
    def __str__(self):
        return self.title
  
        
class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    user=models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text