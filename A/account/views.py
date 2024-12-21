from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.views import View
from .forms import UserRegistrationFrom,UserLoginForem,EditUserProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as authviews
from django.urls import reverse_lazy
from .models import Relation
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

     def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
          self.next = request.GET.get('next')
          return super().setup(request, *args, **kwargs)

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
                if self.next:
                     return redirect(self.next)
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
     login_url='/account/login'
     def get(self,request,user_id):
         is_following=False
         #user = User.objects.get(id=user_id)
         user= get_object_or_404(User,pk=user_id)
         #posts = Post.objects.filter(user=user)
         posts = user.posts.all()
         #posts = get_list_or_404(Post,user=user)
         relation = Relation.objects.filter(from_user=request.user,to_user=user)
         if relation.exists():
              is_following = True

         return render(request,'account\profile.html',{'user':user,'posts':posts,'is_following':is_following})
     

class UserPasswordResetView(authviews.PasswordResetView):
     template_name = 'account/password_reset_form.html'
     success_url = reverse_lazy('account:password_reset_done')
     email_template_name='account/password_reset_email.html'
     
class UserPasswordResetDoneView(authviews.PasswordResetDoneView):
     template_name="account/password_reset_done.html"

class UserPasswordResetConfirmView(authviews.PasswordResetConfirmView):
     template_name='account/password_reset_confirm.html'
     success_url = reverse_lazy('account:password_reset_complete')

class UserPasswordResetCompleteView(authviews.PasswordResetCompleteView):
     template_name='account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin,View):
     def get(self,request,user_id):
          user = User.objects.get(pk=user_id)
          relation = Relation.objects.filter(from_user=request.user,to_user=user)
          if relation.exists():
               messages.error(request,'you are alreade following this user','danger')
          else:
               Relation(from_user=request.user,to_user=user).save() #این هم یک روش دیگر برای ایجاد آبجکت در مدل است
               messages.success(request,'you follow this user','success')
          
          return redirect('account:user_profile',user.id)

class UserUnfollowView(LoginRequiredMixin,View):
     def get(self,request,user_id):
          user=User.objects.get(pk=user_id)
          relation = Relation.objects.filter(from_user=request.user,to_user=user)
          if relation.exists():
               relation.delete()
               messages.success(request,'you unfollow this user','success')
          else:
               messages.error(request,'you are not following this user','danger')
          
          return redirect('account:user_profile',user.id)
     
class EditProfileProfileView(LoginRequiredMixin,View):
     form_class = EditUserProfileForm

     def get(self,request):
          form = self.form_class(instance=request.user.profile,initial={'email':request.user.email})
          return render(request,'account/edit_profile.html',{'form':form})

     def post(self,request):
          form = self.form_class(request.POST,instance=request.user.profile)
          if form.is_valid():
               form.save()
               request.user.email = form.cleaned_data['email']
               request.user.save()
               messages.success(request,'profile edites successfully','success')
          return redirect('account:user_profile',request.user.id)
