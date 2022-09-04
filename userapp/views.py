from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from texnoman.models import Comment, UserProfile,Blog,Tag
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from texnoman.views import Sidebar
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from .form import AddBlogForm
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.
        
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,"Username yoki password noto'g'ri")
            
        return render(request,'login.html')
        
class LogOutBlog(View):
    def get(self,request):
        logout(request)
        return redirect('loginpage')

class SignUpBlog(CreateView):
    form_class = SignUpForm
    template_name = 'regsiter.html'
    success_url = reverse_lazy('loginpage')

class ProfileBlog(Sidebar,View):
    def get(self,request):
        username=request.user.username
        profile=UserProfile.objects.get(username=username)
        blogss=Blog.objects.filter(user=profile)
        comments=Comment.objects.all()
        comment_count=0
        for i in blogss:
            comment_count+=Comment.objects.filter(blog=i).count()
        tags=Tag.objects.all()[:4]
        tags1=Tag.objects.all()[4:]
        blogs=Blog.objects.order_by('-created_at').all()
        users=UserProfile.objects.all()

        context={
            'profile':profile,
            'comment_count':comment_count,
            'tags':tags,
            'tags1':tags1,
            'blogs':blogs,
            'trend_post':self.trending_posts,
            'comments':comments,
            'users':users

        }
        return render(request,'profile.html',context)   

class editprofile(Sidebar,View):
    @method_decorator(login_required(login_url='loginpage'))
    def get(self,request,username):
        user=UserProfile.objects.get(username=username)
        form = UserProfileForm(instance=user)
        username=request.user.username
        profile=UserProfile.objects.get(username=username)
        comments=Comment.objects.all()
        tags=Tag.objects.all()[:4]
        tags1=Tag.objects.all()[4:]
        blogs=Blog.objects.order_by('-created_at').all()
        users=UserProfile.objects.all()

        context={
            'profile':profile,
            'tags':tags,
            'tags1':tags1,
            'blogs':blogs,
            'trend_post':self.trending_posts,
            'comments':comments,
            'users':users,
            'password_form': PasswordChangeForm(request.user),
            'form':form

        }
        return render(request,'editprofile.html',context)
    def post(self,request,username):
        user=request.user
        form = UserProfileForm(request.POST,request.FILES,instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect('editprofiles',user.username)
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('home')
        
        context={

            'password_form': PasswordChangeForm(request.user),
            'form':form
        }
        return render(request,'editprofile.html',context)

class AddBlog(Sidebar,View):
    @method_decorator(login_required(login_url='loginpage'))
    def get(self,request):
        form = AddBlogForm()
        context={
            'form':form,
            'tags':self.tags()
        }
        return render(request,'addblog.html',context)
    def post(self,request):
        if request.method=="POST":
            form=AddBlogForm(request.POST,request.FILES)
            if form.is_valid():
                form_create=form.save(commit=False)
                form_create.slug=slugify(form_create.title)
                form_create.user=request.user
                form_create.save()
                blog = Blog.objects.get(id=form_create.id)
                tagss=form.cleaned_data['tags'].split(',')
                for tag in tagss:
                    tag,create=Tag.objects.get_or_create(name=tag.upper().strip())
                    blog.tags.add(tag)
                return redirect('home')
        return render(request,'addblog.html',{'form':AddBlogForm()})