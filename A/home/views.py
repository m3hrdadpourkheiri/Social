from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

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

    
