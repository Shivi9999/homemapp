from django import forms
from .models import * 

class Userform(forms.ModelForm):
  class Meta:
    model=User
    fields=['username','email','password']
    
    widgets = {
            
              #'user_id': ModelSelect2Widget(model=Add_user, search_fields=['User_Id__icontains']),
              'username': forms.TextInput(attrs={'class': 'form-control'}),
              'email': forms.TextInput(attrs={'class': 'form-control'}),
              'password': forms.TextInput(attrs={'class': 'form-control'}),
              
    
          }
  
class PropertyForm(forms.ModelForm):
  class Meta:
    model=PropertyOwner
    fields=['property_name','address','mobile']
    widgets = {
           
            #'user_id': ModelSelect2Widget(model=Add_user, search_fields=['User_Id__icontains']),
            'property_name': forms.TextInput(attrs={'class': 'form-control', }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
