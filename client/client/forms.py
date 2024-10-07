from django import forms

class Signin(forms.Form):
    email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput({"placeholder":"Enter your email"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Enter your password"}))
    sessionName = forms.CharField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Enter your session name (Optional)"}), required=False)

class Signup(forms.Form):
    email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput({"placeholder":"Enter your email"}))
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Enter your username"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Create a password"}))
    rePassword = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Confirm your password"}))