from django import forms

class Signin(forms.Form):
    email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput({"placeholder":"Enter your email"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Enter your password"}))
    sessionName = forms.CharField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Enter your session name (Optional)"}), required=False)

class Signup(forms.Form):
    email = forms.EmailField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Email", "class":"inputField"}))
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Username", "class":"inputField"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Password", "class":"inputField"}))
    rePassword = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Repeat Password", "class":"inputField"}))