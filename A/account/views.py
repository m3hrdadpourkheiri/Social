from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationFrom
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


class RegisterView(View):
        form_class = UserRegistrationFrom

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
            # else:
            #     messages.success(request,"لطفا اطلاعات را به درسیتی وارد کنید.",'danger')
            return render(request,'account/register.html',{'form':form})
