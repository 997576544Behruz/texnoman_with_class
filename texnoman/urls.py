from django.urls import path
from .views import *

urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('category/<slug:slug>', CategoryBlogs.as_view(), name='category'),
    path('tag/<slug:slug>', TagBlogs.as_view(), name='tag'),
    path('detail/<slug:slug>', DetailBlog.as_view(), name='detail'),
    path('search/', SearchBlog.as_view(), name='search'),
    path('updateblog/<slug:slug>',UpdateBlog.as_view(),name='updateblog'),
    path('deleteblog/<slug:slug>',DeleteBlog.as_view(),name='deleteblog'),
    path('users/',UsersBlog.as_view(),name='userss')
]