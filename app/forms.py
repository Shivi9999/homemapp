from django import forms
from .models import * 
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
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


class QuestionForm(forms.ModelForm):
    excel_file = forms.FileField(required=False)

    class Meta:
        model = QuestionAnswer
        fields = ['question', 'answer']

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control','required': False}),
            'answer': forms.TextInput(attrs={'class': 'form-control','required': False}),
        }

   

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styles or attributes if needed

    # def clean_old_password(self):
    #     old_password = self.cleaned_data.get('old_password')
    #     # Perform additional validation if needed
    #     return old_password
    def clean_old_password(self):
            old_password = self.cleaned_data.get('old_password')

            # Check if the old password matches the user's current password
            if not self.user.check_password(old_password):
                raise ValidationError("The old password is incorrect.")

            # Perform additional validation if needed
            return old_password
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        # Perform additional validation if needed
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("The two password fields didn't match.")

        # Perform additional validation if needed
        return new_password2

    

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Select an Excel file')




