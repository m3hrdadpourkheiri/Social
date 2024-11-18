from django import forms


class UserRegistrationFrom(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()