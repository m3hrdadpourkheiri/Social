from django import forms


class UserRegistrationFrom(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your username'}),label='نام کاربری',error_messages={'required':'لطفا نلم کاربری را وارد کنید'})
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Example@email.com'}),label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your password'}),label='کلمه عبور')