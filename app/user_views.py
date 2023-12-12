from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
import pandas as pd
from django. contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout, login as auth_login


@login_required(login_url='login')
def user_dashboard(request):
    return render(request,'Owner/index.html')




@login_required(login_url='login')
def add_user_management(request):
    if request.method == "POST":
        form = Userform(request.POST)
        user_form= Add_userform(request.POST,request.FILES)
        
        if form.is_valid() and user_form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            print("Form Data:", form.cleaned_data)
            form.instance.user_type = '3'
            print()
            user_instance = form.save(commit=False)
            # Set the user type statically
            user_instance.set_password(password)
            user_instance.save()
            saved_user = User.objects.get(pk=user_instance.pk)
            print("Saved User Type:", saved_user.user_type)
            owner_instance = user_form.save(commit=False)
            owner_instance.user = user_instance
            owner_instance.save()
            
            return redirect('View_user_management')
        else:
            print(form.errors)
            print(user_form.errors)
            return render(request, 'Owner/user_management_add.html', {'form': form,'user_form': user_form})
    form = Userform()
    user_form = Add_userform()
   
    return render(request,'Owner/user_management_add.html',{'form': form,'user_form': user_form})

@login_required(login_url='login')    
def view_user_management(request):
    user_management=Add_user.objects.all()
    return render(request,'Owner/user_management_view.html',{'user_management':user_management})

@login_required(login_url='login')
def edit_user(request, id):
    property_owner = get_object_or_404(Add_user, pk=id)

    if request.method == 'POST':
        user_form = Userform(request.POST, instance=property_owner.user)
        property_form = Add_userform(request.POST, instance=property_owner)

        if user_form.is_valid() and property_form.is_valid():
            user_form.save()
            property_form.save()

            messages.success(request, 'User  updated successfully.')
            return redirect('View_user_management')
        else:
            messages.error(request, 'Error updating property owner. Please check the form.')
            print(user_form.errors)
            print(property_form.errors)
    else:
        user_form = Userform(instance=property_owner.user)
        property_form = Add_userform(instance=property_owner)

  
    return render(request, 'Owner/edit_user.html', {'user_form': user_form, 'property_form': property_form})

@login_required(login_url='login')
def delete_user(request, id):
    user1 = get_object_or_404(Add_user, pk=id)
    
    # Retrieve the associated user
    user_instance = user1.user
    print(user_instance)
    # Delete the property owner and associated user
    user1.delete()
    user_instance.delete()
    return redirect('View_user_management')







@login_required(login_url='login')    
def add_room(request):
    return render(request,'Owner/rooms_add_room.html')

@login_required(login_url='login')
def view_room(request):
    return render(request,'Owner/rooms_view_room.html')

@login_required(login_url='login')
def faq_view(request):
   
    if request.method=="POST":
        faq_form = Faqform(request.POST)
        if faq_form.is_valid():
            faq=faq_form.save(commit=False)
            faq.save()
            return redirect('Faq')
        else:
            print(faq_form.errors)
            return render(request,'Owner/faq.html',{'faq_form':faq_form})
    faq_form=Faqform(request.POST)
    faq=Faq.objects.all()      
    return render(request,'Owner/faq.html',{'faq_form':faq_form,'faq':faq})

@login_required(login_url='login')
def terms_condition_user(request):
    terms_data = TermsCondition.objects.all()
    return render(request,'Owner/terms_condition.html',{'terms_data':terms_data})

@login_required(login_url='login')
def privacy_policy_user(request):
    fetch_privacy=PrivacyPolicy.objects.all()
    return render(request,'Owner/privacy_policy.html',{'fetch_privacy':fetch_privacy})

@login_required(login_url='login')
def Notification_user(request):
    return render(request,'Owner/Notification.html')


@login_required(login_url='login')
def profile_user(request):
    return render(request,'Owner/profile.html')