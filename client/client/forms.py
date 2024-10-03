from django import forms

class Signin(forms.Form):
    email = forms.EmailField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Email", "class":"inputField"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Password", "class":"inputField"}))