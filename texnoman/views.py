from django.shortcuts import render,redirect
from django.views import View
from .forms import CommentForm, UpdateBlogForm
from .models import *
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

class Sidebar:
    def categories(self):
        return Category.objects.all()
    def tags(self):
        return Tag.objects.all()
    
    def trending_posts(self):
        return Blog.objects.order_by("-views")[:3]

class Home(Sidebar, View):
    def get(self, request):
        blogs = Blog.objects.all()
        p = Paginator(blogs, 2)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)

        context = {
            'blogs':page_obj
        }
        context['categories'] = self.categories()
        context['tags'] = self.tags()
        context['trending_posts'] = self.trending_posts()
        return render(request, "home.html", context)

class CategoryBlogs(Sidebar, View):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        context = {}
        context['blogs'] = Blog.objects.filter(category=category)
        context['category'] = category
        context['categories'] = self.categories()
        context['tags'] = self.tags()
        context['trending_posts'] = self.trending_posts()
        return render(request, "home.html", context)
    
class TagBlogs(Sidebar, View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        context = {}
        context['blogs'] = Blog.objects.filter(tags=tag)
        context['category'] = tag
        context['categories'] = self.categories()
        context['tags'] = self.tags()
        context['trending_posts'] = self.trending_posts()
        return render(request, "home.html", context)

class DetailBlog(Sidebar, View):
    def get(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        blog.views += 1
        blog.save()
        context = {}
        context['blog'] = blog
        context['categories'] = self.categories()
        context['tags'] = self.tags()
        context['trending_posts'] = self.trending_posts()
        context['form'] = CommentForm()
        return render(request, "detail.html", context)
    def post(self,request,slug):
        blog=Blog.objects.get(slug=slug)
        if request.method=="POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                form_comment=form.save(commit=False)
                form_comment.blog=blog
                form_comment.user=request.user
                form_comment.save()
                return redirect('detail',slug=blog.slug)
            else:
                form=CommentForm()
        context = {}
        context['blog'] = blog
        context['categories'] = self.categories()
        context['tags'] = self.tags()
        context['trending_posts'] = self.trending_posts()
        context['form'] = CommentForm()
        return render(request, "detail.html", context)


class SearchBlog(Sidebar, View):
    def post(self, request):
        query = request.POST.get('search')
        category = Category.objects.filter(name__icontains=query)
        blogs = Blog.objects.filter(title__icontains = query) | Blog.objects.filter(content__icontains=query) | \
            Blog.objects.filter(category__in = category)
        context = {}
        context['blogs'] = blogs
        context['categories'] = self.categories()
        context['tags'] = self.tags()
        context['trending_posts'] = self.trending_posts()
        return render(request, "home.html", context)
      
class UpdateBlog(View):
    @method_decorator(login_required(login_url='loginpage'))
    def get(self,request,slug):
        blog = Blog.objects.get(slug=slug)
        form=UpdateBlogForm(instance=blog)
        satr=""
        for tag in blog.tags.all():
            satr+=str(tag)+','
        f=satr[0:(len(satr)-1)]
        context={
            'form':form,
            'satr':f,
        }

        return render(request,'updateblog.html',context)
    def post(self,request,slug):

        blog=Blog.objects.get(slug=slug)
        form=UpdateBlogForm(request.POST,request.FILES,instance=blog)

        if form.is_valid():
            form_update=form.save(commit=False)
            form_update.user=request.user
            form_update.slug=slugify(form_update.title)
            form_update.save()
            tagsss=Tag.objects.all()
            blog.tags.clear()
            for tagss in tagsss:
                blogs = Blog.objects.filter(tags=tagss).exists()
                if not blogs:
                        tagss.delete()
            tags=request.POST.get('tags').split(',')
            for tag in tags:
                tag,create=Tag.objects.get_or_create(name=tag.upper().strip())
                if not tag in blog.tags.all():
                    blog.tags.add(tag)            
            return redirect('detail',blog.slug)
        satr=""     
        for tag in blog.tags.all():
            satr+=str(tag)+','
        f=satr[0:(len(satr)-1)]
        context={
            'satr':f,
            'form':UpdateBlogForm(instance=blog)
        }
        return render(request,'updateblog.html',context)
        
class DeleteBlog(View):
    @method_decorator(login_required(login_url='loginpage'))
    def get(self,request,slug):
        blog = Blog.objects.get(slug=slug)
        context={
            'blog':blog
        }
        return render(request,'deleteblog.html',context)

    def post(self,request,slug):
        blog = Blog.objects.get(slug=slug)
        blog.delete()
        tags=Tag.objects.all()
        for tag in tags:
            blog=Blog.objects.filter(tags=tag).exists()
            if not blog:
                tag.delete()
        return redirect('home')



class UsersBlog(View):
    def get(self,request):
        users=UserProfile.objects.order_by('-last_login')
        context={
            'users':users,
        }
        return render(request,'users.html',context)

