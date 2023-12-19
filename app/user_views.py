from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
import pandas as pd
from django. contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout, login as auth_login
from django.http import JsonResponse

@login_required(login_url='login_user')
def user_dashboard(request):
    return render(request,'Owner/index.html')




@login_required(login_url='login_user')
def add_hotel_management(request):
    if request.method == 'POST':
        form = AddHotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.user = request.user
            hotel.save()
            return redirect('view_hotel_management')
        else:
            print(form.errors)
            return render(request, 'Owner/hotel_Add_management.html', {'form': form})
    else:
        form = AddHotelForm()

    return render(request, 'Owner/hotel_Add_management.html', {'form': form})

           
   
    


@login_required(login_url='login_user')
def view_hotel_management(request):
    
    hotel_view = Add_hotel.objects.filter(user=request.user)
   
    return render(request,'Owner/view_hotel_managment.html',{'hotel_view':hotel_view})

@login_required(login_url='login_user')
def edit_hotel(request, id):
    hotel = Add_hotel.objects.get(id=id)

    if request.method == 'POST':
        form = AddHotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('view_hotel_management')  # replace with your URL name
    else:
        form = AddHotelForm(instance=hotel)

    return render(request, 'Owner/edit_hotel.html', {'form': form, 'hotel': hotel})


@login_required(login_url='login_user')
def delete_hotel(request, id):
    user1 = get_object_or_404(Add_hotel, pk=id)
    # Retrieve the associated user
    
    user1.delete()
    
    return redirect('view_hotel_management')






@login_required(login_url='login_user')
def add_property_management(request):
   
    if request.method == 'POST':
        form = AddRoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_property_management')  # Assuming you have a URL pattern named 'room_list' for displaying the list of rooms
        else:
           print(form.errors )
    else:
        form = AddRoomForm()

   
    return render(request,'Owner/property_Add_Management.html',{'form': form})



@login_required(login_url='login_user')
def view_property_management(request):
    hotels = Add_hotel.objects.filter(user=request.user)
    
    # Fetch rooms associated with the hotels of the logged-in user
    property_management = Add_Room.objects.filter(flat_name__in=hotels)
   
    return render(request,'Owner/View_property_managment.html',{'property_management':property_management})

@login_required(login_url='login_user')
def edit_room(request, id):
    room = Add_Room.objects.get(id=id)

    if request.method == 'POST':
        form = AddRoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('view_property_management')  # replace with your URL name
    else:
        form = AddRoomForm(instance=room)

    return render(request, 'Owner/edit_room.html', {'form': form, 'room': room})





@login_required(login_url='login_user')
def delete_property_management(request,id):
    property_manage = get_object_or_404(Add_Room, id=id)
    
    property_manage.delete()
        

    return JsonResponse({'msg': True})


@login_required(login_url='login_user')
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

@login_required(login_url='login_user')    
def view_user_management(request):
    user_management=Add_user.objects.all()
    return render(request,'Owner/user_management_view.html',{'user_management':user_management})

@login_required(login_url='login_user')
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

@login_required(login_url='login_user')
def delete_user(request, id):
    user1 = get_object_or_404(Add_user, pk=id)
    
    # Retrieve the associated user
    user_instance = user1.user
    print(user_instance)
    # Delete the property owner and associated user
    user1.delete()
    user_instance.delete()
    return redirect('View_user_management')



def login_user(request):
    # Print the entire session dictionary
    print(request.session)



    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful.')

           

            if user.user_type == '2':
                # Access and print user_session_id
                request.session['user_session_id'] = user.id
                user_session_id = request.session.get('user_session_id')
                print(f"User Session ID: {user_session_id}")

                return redirect('user_dashboard')  # User dashboard

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Owner/login.html')



def logout_view_user(request):
   # Clear the session
    logout(request)

    # Optionally, you can delete the sessionid cookie
    response = redirect('login_user')
    response.delete_cookie('sessionid')  # Replace 'your_logout_redirect_view' with the actual logout redirect view
    return response


@login_required(login_url='login_user')    
def add_room(request):
    return render(request,'Owner/rooms_add_room.html')

@login_required(login_url='login_user')
def view_room(request):
    return render(request,'Owner/rooms_view_room.html')

@login_required(login_url='login_user')
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
    faqs=Faq.objects.all()      
    return render(request,'Owner/faq.html',{'faq_form':faq_form,'faqs':faqs})

def edit_faq(request, id):
    faq = get_object_or_404(Faq, pk=id)
    if request.method == 'POST':
        form = Faqform(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect('Faq')
    else:
        faq_form = Faqform(instance=faq)
    return render(request, 'Owner/edit_faq.html', {'faq_form': faq_form, 'faq': faq})



@login_required(login_url='login_user')
def delete_faq(request, id):
    faq = get_object_or_404(Faq, pk=id)
    
    faq.delete()
    return redirect('Faq')



@login_required(login_url='login_user')
def terms_condition_user(request):
    terms_data = TermsCondition.objects.all()
    return render(request,'Owner/terms_condition.html',{'terms_data':terms_data})

@login_required(login_url='login_user')
def privacy_policy_user(request):
    fetch_privacy=PrivacyPolicy.objects.all()
    return render(request,'Owner/privacy_policy.html',{'fetch_privacy':fetch_privacy})

@login_required(login_url='login_user')
def Notification_user(request):
    return render(request,'Owner/Notification.html')


@login_required(login_url='login_user')
def profile_user(request):
    # Retrieve the PropertyOwner instance related to the logged-in user
    owner_profile = get_object_or_404(PropertyOwner, user=request.user)

    profile_form = Userform(instance=request.user)
    owner_form = PropertyForm(instance=owner_profile)

    form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'Owner/profile.html', {'profile_form': profile_form, 'form': form, 'owner_form': owner_form})


@login_required(login_url='login_user')
def update_personal_details_user(request):
    owner_profile = get_object_or_404(PropertyOwner, user=request.user)
    profile_form = Userform(instance=request.user)
    owner_form = PropertyForm(instance=owner_profile)

    if request.method == 'POST':
        # Create the forms with modified POST data
        profile_form = Userform(request.POST, instance=request.user)
        owner_form = PropertyForm(request.POST, instance=owner_profile)

        if profile_form.is_valid() and owner_form.is_valid():
            owner_form.save()
            profile_form.save()
            messages.success(request, 'Personal details updated successfully!')
        else:
            print(profile_form.errors)
            print(owner_form.errors)
            messages.error(request, 'Error updating personal details. Please check the form.')

    return redirect('Profile_user')


@login_required(login_url='login_user')
def change_password_user(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
        else:
            print(form.errors)
            messages.error(request, 'Error changing password. Please check the form.')
            return render(request,'Owner/profile.html',{'form':form})

    return redirect('Profile_user')