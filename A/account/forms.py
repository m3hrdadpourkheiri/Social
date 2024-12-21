from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserLoginForem(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your username'}),label='نام کاربری')
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your username'}),label='کلمه عبور')


class UserRegistrationFrom(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your username'}),label='نام کاربری')
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Example@email.com'}),label='ایمیل')
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your password'}),label='کلمه عبور')
    confirm_password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your password'}),label='تایید کلمه عبور')


    def clean_username(self):
        username=self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username already exist')
        return username
    
    def clean_email(self):
        email=self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exist')
        return email
    
    def clean(self):
        cd = super().clean()
        password = cd.get('password')
        confirmpassword = cd.get('confirm_password')
        if password and confirmpassword and password != confirmpassword:
            raise ValidationError('کلمه عبور و تایید کلمه عبور باید یکسان باشند')
        

class EditUserProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta():
        model = Profile
        fields = ('age','bio',)

    