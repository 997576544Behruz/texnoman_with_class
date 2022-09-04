from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(UserProfile)
class Userprofilemodel(admin.ModelAdmin):
    list_display=['username','birthday', 'address', 'phone_number']
@admin.register(Blog)
class CategoryModel(admin.ModelAdmin):
    list_display=['title','created_at']
    prepopulated_fields={'slug':('title',)}

@admin.register(Category)
class CategoryModel(admin.ModelAdmin):
    list_display=['name','created_at']
    prepopulated_fields={'slug':('name',)}
@admin.register(Tag)
class TagModel(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
    
@admin.register(Comment)
class TagModel(admin.ModelAdmin):
    list_display=['text']
