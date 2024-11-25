from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm,PostNewForm
from django.utils.text import slugify
# Create your views here.


class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request,'home/index.html',{'posts':posts})
    

class PostView(LoginRequiredMixin,View):
    login_url='/account/login'
    def get(self,request,post_id,post_slug):
        post = Post.objects.get(pk=post_id)
        return render(request,'home/detail.html',{'post':post})

class PostDeleteView(LoginRequiredMixin,View):
    login_url='/account/login'
    def get(self,request,post_id):
         post = Post.objects.get(id=post_id)
         if request.user.id == post.user.id:
             post.delete()
             messages.success(request,'پست بطور کامل پاک شد.','info')
             return redirect('home:home')
         messages.error(request,'شما نمی توانید این پست را حذف کنید.','danger')
         return redirect('home:home')
    

class PostUpdateView(LoginRequiredMixin,View):
     form_class  = PostUpdateForm

     def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
         self.post_instance= Post.objects.get(pk=kwargs['post_id'])
         return super().setup(request, *args, **kwargs)
     
     def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
         post = self.post_instance
         if not post.user.id == request.user.id:
             messages.error(request,'access denied','danger')
             return redirect('home:home')
         return super().dispatch(request, *args, **kwargs)
     

     def get(self,request,post_id):
         post = self.post_instance
         form = self.form_class(instance=post)
         return render(request,'home/update.html',{'form':form})

     def post(self,request,post_id):
         post = self.post_instance
         form=self.form_class(request.POST,instance=post)
         if form.is_valid:
             updated_post = form.save(commit=False)
             updated_post.slug = slugify(form.cleaned_data['title'][:30])
             updated_post.save()
             messages.success(request,'بروز رسانی شد','success')
             return render(request,'home/detail.html',{'post':post})
         


class NewPostView(LoginRequiredMixin,View):
    form_class = PostNewForm

    def get(self,request):
        form = self.form_class
        return render(request,'home/new.html',{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request,'پست اضافه شد','success')
            return redirect('home:post_detail',new_post.id,new_post.slug)
        
         
    
