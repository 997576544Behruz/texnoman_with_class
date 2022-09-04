from django.urls import path
from .views import *

urlpatterns=[
    path('',LoginView.as_view(),name='loginpage'),
    path('logout/',LogOutBlog.as_view(),name='logout'),
    path('sign/',SignUpBlog.as_view(),name='signin'),
    path('profile/',ProfileBlog.as_view(),name='profile'),
    path('editprofile/<slug:username>',editprofile.as_view(),name='editprofiles'),
    path('addblog/',AddBlog.as_view(),name='addblog')
    


]