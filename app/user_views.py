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



def logout_view_user(request):
    logout(request)
    # Optionally add a success message or perform other actions
    return redirect('login')


@login_required(login_url='login')
def add_user_management(request):
    return render(request,'Owner/user_management_add.html')

@login_required(login_url='login')    
def view_user_management(request):
    return render(request,'Owner/user_management_view.html')

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
    return render(request,'Owner/terms_condition.html')

@login_required(login_url='login')
def privacy_policy_user(request):
    return render(request,'Owner/privacy_policy.html')

@login_required(login_url='login')
def Notification_user(request):
    return render(request,'Owner/Notification.html')



@login_required(login_url='login')
def profile_user(request):
    return render(request,'Owner/profile.html')