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
            # Get the username and password from the userform
            full_name = userform.cleaned_data['full_name']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']
            
            # Create a new user instance
            user_instance = User.objects.create_user(full_name=full_name, password=password,email=email)
            
            owner_instance = ownerform.save(commit=False)
            
            # Associate the user with the owner
            owner_instance.user = user_instance
            owner_instance.save()
            
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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Using authenticate function with username (assuming full_name is the username field)
        user = authenticate(request, email=email, password=password)

        if user is not None:

            dj_login(request, user)
            return redirect('owner_home')  # Replace 'index' with the actual URL or name of your index page
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

def owner_home(request):
    
    return render(request,'owner_home.html')



def add_hotel(request):
    if request.method == "POST":
        hotelform = Hotelform(request.POST)
        if hotelform.is_valid():
            hotelform.save()
            return redirect('add_hotel')
        else:
            print("Form is not valid. Errors:", hotelform.errors)
    else:
        hotelform = Hotelform()

    return render(request, 'add_hotel.html', {'hotelform': hotelform})
