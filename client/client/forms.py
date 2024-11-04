from django import forms
from django.core.validators import FileExtensionValidator

class Signin(forms.Form):
    email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput({"placeholder":"Enter your email"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Enter your password"}))
    sessionName = forms.CharField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Enter your session name (Optional)"}), required=False)

class Signup(forms.Form):
    email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput({"placeholder":"Enter your email"}))
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Enter your username"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Create a password"}))
    rePassword = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Confirm your password"}))

class VaultNew(forms.Form):
    name = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the name"}), required=False)
    username = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the username"}), required=False)
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Create a password"}), required=False)
    url = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the url"}), required=False)

class VaultDelete(forms.Form):
    id = forms.IntegerField(label="", widget=forms.NumberInput({"placeholder":"Enter the ID"}))

class VaultEdit(forms.Form):
    id = forms.IntegerField(label="", widget=forms.NumberInput({"placeholder":"Enter the ID", "id":"id_popup-edit-id"}))
    newName = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the name"}))
    newUsername = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the username"}))
    newPassword = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Create a password"}))
    newUrl = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the url"}), required=False)

class SessionEdit(forms.Form):
    sessionIdW = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the session idw"}))
    newSessionName = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the name"}))

class SessionDelete(forms.Form):
    SessionDeleteSessionIdW = forms.CharField(label="", max_length=100, widget=forms.TextInput({"placeholder":"Enter the session idw"}))

class ImageUpdate(forms.Form):
    image = forms.ImageField(
    label="Profile Picture",
    max_length=15,
    validators=[FileExtensionValidator(allowed_extensions=['jpg'])],
    widget=forms.FileInput(attrs={'accept': '.jpg'}),
)