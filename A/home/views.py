from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Post,Comment,Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm,PostNewForm,CommentCreateForm,CommentReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class HomeView(View):
    def get(self,request):
        #posts = Post.objects.all().order_by('-created')
        posts = Post.objects.order_by('-created')
        return render(request,'home/index.html',{'posts':posts})
    

class PostView(View):
    login_url='/account/login'
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instance = get_object_or_404(Post,pk=kwargs['post_id'],slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    

    def get(self,request,post_id,post_slug):
        #post = Post.objects.get(pk=post_id)
        post = get_object_or_404(Post,pk=post_id)
        comments = self.post_instance.pcomments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like=True
        return render(request,'home/detail.html',{'post':self.post_instance,'comments':comments,'form':self.form_class,'reply_form':self.form_class_reply,'can_like':can_like})
    
    @method_decorator(login_required) #part 36 method decorators
    def post( self,request,*args,**kwargs):

        form=self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request,'comment added successfully','success')
            return redirect('home:post_detail',self.post_instance.id,self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin,View):
    login_url='/account/login'
    def get(self,request,post_id):
         #post = Post.objects.get(id=post_id)
         post = get_object_or_404(Post,pk=post_id)
         if request.user.id == post.user.id:
             post.delete()
             messages.success(request,'پست بطور کامل پاک شد.','info')
             return redirect('home:home')
         messages.error(request,'شما نمی توانید این پست را حذف کنید.','danger')
         return redirect('home:home')
    

class PostUpdateView(LoginRequiredMixin,View):
     form_class  = PostUpdateForm

     def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
         #self.post_instance= Post.objects.get(pk=kwargs['post_id'])
         self.post_instance = get_object_or_404(Post,pk=kwargs['post_id'])
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
        
         
class PostAddReplyView(LoginRequiredMixin,View):
    form_class = CommentReplyForm

    def post(self,request,post_id,comment_id):
        post = get_object_or_404(Post,id=post_id)
        comment = get_object_or_404(Comment,pk=comment_id)
        form=self.form_class(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.user=request.user
            reply.post = post
            reply.reply = comment
            reply.is_replu = True
            reply.save()
            messages.success(request,'reply submited successfully','success')
        return redirect('home:post_detail',post.id,post.slug)

class PostLikeView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = get_object_or_404(Post,pk=post_id)
        like = Vote.objects.filter(post = post,user=request.user)
        if like.exists():
            messages.error(request,'you already liked this post.','danger')
        else:
            Vote.objects.create(post=post,user=request.user)
            messages.success(request,'you like this post successfully')
        return redirect('home:post_detail', post.id,post.slug)

    
        
    
