from django import forms
from .models import *
class Userform(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','full_name','password']

class Ownerform(forms.ModelForm):

    class Meta:
        model=HotelOwner
        fields=['address','mobile']