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
    note = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the note"}), required=False)

class VaultDelete(forms.Form):
    id = forms.IntegerField(label="", widget=forms.NumberInput({"placeholder":"Enter the ID"}))

class VaultEdit(forms.Form):
    id = forms.IntegerField(label="", widget=forms.NumberInput({"placeholder":"Enter the ID", "id":"id_popup-edit-id"}), required=False)
    newName = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the name"}), required=False)
    newUsername = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the username"}), required=False)
    newPassword = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Create a password"}), required=False)
    newUrl = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the url"}), required=False)
    newNote = forms.CharField(label="",  max_length=100, widget=forms.TextInput({"placeholder":"Enter the note"}), required=False)

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
    
    def clean_image(self):
        image = self.cleaned_data['image']
        if len(image.name) > 15:
            raise forms.ValidationError("File name should not exceed 15 characters")
        return image
    
class PGConfig(forms.Form):
    length = forms.IntegerField(label="", min_value=1, max_value=100, widget=forms.NumberInput({"placeholder":"Enter the length"}))
    capitalLetters = forms.BooleanField(label="", widget=forms.CheckboxInput({"placeholder":"Should contain capital letters"}), required=False)
    smallLetters = forms.BooleanField(label="", widget=forms.CheckboxInput({"placeholder":"Should contain small letters"}), required=False)
    numbers = forms.BooleanField(label="", widget=forms.CheckboxInput({"placeholder":"Should contain numbers"}), required=False)
    symbols = forms.BooleanField(label="", widget=forms.CheckboxInput({"placeholder":"Should contain symbols"}), required=False)

class ImportVault(forms.Form):
    file = forms.FileField(
    label="Import Vault",
    max_length=60,
    validators=[FileExtensionValidator(allowed_extensions=['json'])],
    widget=forms.FileInput(attrs={'accept': '.json'}),
)
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if len(file.name) > 60:
            raise forms.ValidationError("File name should not exceed 60 characters")
        return file
    
class Otp(forms.Form):
    otp1 = forms.IntegerField(label="", min_value=0, max_value=9, widget=forms.NumberInput({"type":"text", "class":"otp-box", "id":"otp1"}))
    otp2 = forms.IntegerField(label="", min_value=0, max_value=9, widget=forms.NumberInput({"type":"text", "class":"otp-box", "id":"otp2"}))
    otp3 = forms.IntegerField(label="", min_value=0, max_value=9, widget=forms.NumberInput({"type":"text", "class":"otp-box", "id":"otp3"}))
    otp4 = forms.IntegerField(label="", min_value=0, max_value=9, widget=forms.NumberInput({"type":"text", "class":"otp-box", "id":"otp4"}))
    otp5 = forms.IntegerField(label="", min_value=0, max_value=9, widget=forms.NumberInput({"type":"text", "class":"otp-box", "id":"otp5"}))
    otp6 = forms.IntegerField(label="", min_value=0, max_value=9, widget=forms.NumberInput({"type":"text", "class":"otp-box", "id":"otp6"}))

class ChangePassword(forms.Form):
    oldPassword = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Enter your old password"}))
    newMasterPassword = forms.CharField(label="", max_length=100, widget=forms.PasswordInput({"placeholder":"Enter your new password"}))