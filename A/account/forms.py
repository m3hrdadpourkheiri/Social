from django import forms


class UserRegistrationFrom(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your username'}),label='نام کاربری')
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Example@email.com'}),label='ایمیل')
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your password'}),label='کلمه عبور')