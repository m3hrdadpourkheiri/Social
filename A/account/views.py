from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationFrom,UserLoginForem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
# Create your views here.

class UserLogoutView(LoginRequiredMixin,View):
    login_url='/account/login'
     
    def get(self,request):
          logout(request)
          messages.success(request,'شما از حساب خود خارج شدید','info')
          return redirect('home:home')



class UserLoginView(View):
     form_class = UserLoginForem
     template_name= 'account/login.html'

     def dispatch(self, request, *args: Any, **kwargs: Any):
           if request.user.is_authenticated:
                return redirect('home:home')
           return super().dispatch(request, *args, **kwargs)

     def get(self,request):
          form=self.form_class
          return render(request,self.template_name,{'form':form})
     
     def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully','success')
                return redirect('home:home')
            messages.success(request,'username or password is wrong','danger')
        return render(request,self.template_name,{'form':form})
          

class UserRegisterView(View):
        form_class = UserRegistrationFrom

        def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
          if request.user.is_authenticated:
               return redirect('home:home')
          return super().dispatch(request, *args, **kwargs)

        def get(self,request):
            form = self.form_class()
            return render(request,'account/register.html',{'form':form})
        

        def post(self,request):
            
            form = self.form_class(request.POST)
            
            # if User.objects.filter(username = request.POST['username']).exists():
            #      messages.success(request,'Username alredy exist','info')
            #      return render(request,'account/register.html',{'form':form})


            if form.is_valid():
                cd = form.cleaned_data
                User.objects.create_user(cd['username'],cd['email'],cd['password'])
                messages.success(request,'you registered successfully','success')
                return redirect('home:home')
            
            return render(request,'account/register.html',{'form':form})
        

class UserProfileView(LoginRequiredMixin,View):
     def get(self,request,user_id):
         user = User.objects.get(id=user_id)
         posts = Post.objects.filter(user=user)
         return render(request,'account\profile.html',{'user':user,'posts':posts})
     
     