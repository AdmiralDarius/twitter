from django import forms

class UploadFileForm(forms.Form):
    avatar_pic = forms.ImageField()