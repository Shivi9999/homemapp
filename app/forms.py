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
              'password': forms.PasswordInput(attrs={'class': 'form-control'}),
         
          }
  
class PropertyForm(forms.ModelForm):
  class Meta:
    model=PropertyOwner
    fields=['property_name','address','mobile']
    widgets = {
           
            #'user_id': ModelSelect2Widget(model=Add_user, search_fields=['User_Id__icontains']),
            'property_name': forms.TextInput(attrs={'class': 'form-control', }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            
            
        }
  mobile = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True  # Set this to True if mobile is a required field
    )


class QuestionForm(forms.ModelForm):
    excel_file = forms.FileField(required=False)

    class Meta:
        model = QuestionAnswer
        fields = ['hotel','room','question', 'answer']

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control','required': False}),
            'answer': forms.TextInput(attrs={'class': 'form-control','required': False}),
        }
    hotel = forms.ModelMultipleChoiceField(
        queryset=Add_hotel.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox-list'}),
    )
    room = forms.ModelMultipleChoiceField(
        queryset=Add_Room.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox-list'}),
    )
    
    def clean_question(self):
        # Cleaned data for the 'question' field
        question = self.cleaned_data['question']

        # Check if the instance is being created (new record)
        if self.instance is None or self.instance.pk is None:
            # Check if the question already exists in the database
            if QuestionAnswer.objects.filter(question__iexact=question).exists():
                raise forms.ValidationError("This question already exists.")

        return question

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

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'users']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.exclude(user_type='1'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox-list'}),
    )

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['users'].initial = User.objects.exclude(user_type='1').values_list('id', flat=True)

class Faqform(forms.ModelForm):
    
    class Meta:
        model = Faq
        fields = "__all__"


        widgets = {
            
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Add_userform(forms.ModelForm):
  class Meta:
    model=Add_user
    fields=['address','mobile','hotel_name','room_number','user_image']
    widgets = {
            'hotel_name': forms.Select(attrs={'class': 'form-control'}),
            #'user_id': ModelSelect2Widget(model=Add_user, search_fields=['User_Id__icontains']),
            'room_number': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
          
            
            
        }
  mobile = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
          # Set this to True if mobile is a required field
    )

class AddHotelForm(forms.ModelForm):
    class Meta:
        model = Add_hotel
        fields = ['property_name', 'total_room', 'email', 'address', 'mobile', 'flat_image']
        widgets = {
            
                'property_name': forms.TextInput(attrs={'class': 'form-control'}),
                'total_room': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.TextInput(attrs={'class': 'form-control'}),
                'address': forms.TextInput(attrs={'class': 'form-control'}),
            
    
                
            }
    mobile = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
          # Set this to True if mobile is a required field
    )
   

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Add_Room
        fields = ['flat_name', 'room_number', 'room_name', 'room_description', 'room_image']
        widgets = {
            'flat_name': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_name': forms.TextInput(attrs={'class': 'form-control'}),
            'room_description': forms.TextInput(attrs={'class': 'form-control'}),
            'room_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CSVUploadForm(forms.Form):
    file = forms.FileField()


class AddItemsForm(forms.ModelForm):
    class Meta:
        model = Add_items
        fields = ['select_hotel', 'select_room', 'items']
        widgets = {
            'select_hotel': forms.Select(attrs={'class': 'form-control'}),
            'select_room': forms.TextInput(attrs={'class': 'form-control'}),        
            'items': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)