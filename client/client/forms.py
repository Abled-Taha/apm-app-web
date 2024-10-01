from django import forms

class Signin(forms.Form):
    email = forms.EmailField(label="email", max_length=100)
    password = forms.CharField(label="password", max_length=100, widget=forms.PasswordInput)