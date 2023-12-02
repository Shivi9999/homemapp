from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login as dj_login
# Create your views here.
def home(request):
    return render(request,'index.html')


def add_owner(request):
    if request.method == "POST":
        userform = Userform(request.POST)
        ownerform = Ownerform(request.POST)
       
        if userform.is_valid() and ownerform.is_valid():
            user_instance = userform.save()  
            owner_instance = ownerform.save(commit=False)  
            
            # Associate the user with the owner
            owner_instance.user = user_instance
            owner_instance.save()  # Save the owner form with the associated user
            
            return redirect('user_management_view.html')
        else:
            print(userform.errors)
            print(ownerform.errors)

    userform = Userform()
    ownerform = Ownerform()
    return render(request, 'user_management_add.html', {'userform': userform, 'ownerform': ownerform})

def view_owner(request):
    owner=HotelOwner.objects.all()
    context={'owner':owner}
    return render(request,'user_management_view.html',context)

def login(request):
    if request.method=='POST':
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        
        user=authenticate(request,
                                       full_name=request.POST.get('full_name'),
                                       password=request.POST.get('password'))
        
        if user!=None:
            dj_login(request,user) 
            return render('index.html')  
            
        else:
            messages.error(request,'invalid credentials')

    
    return render(request,'login.html')

