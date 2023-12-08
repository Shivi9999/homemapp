from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django. contrib import messages
from django.contrib.auth import authenticate, login as dj_login
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

def dashboard(request):
    property_owner_count=PropertyOwner.objects.all().count()
    context={'property_owner_count':property_owner_count}
    return render(request,'index.html',context)

def login(request):
    return render(request,'login.html')

def add_property_owner(request):
    if request.method == "POST":
        user_form = Userform(request.POST)
        property_form = PropertyForm(request.POST)
        
        if user_form.is_valid() and property_form.is_valid():
            username = user_form.cleaned_data['username']
           
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']

            user_instance = User.objects.create_user(username=username, email=email,password=password)
            
            owner_instance = property_form.save(commit=False)
            owner_instance.user = user_instance
            owner_instance.save()
            
            return redirect(view_property_owner)
        else:
            print(user_form.errors)
            print(property_form.errors)

    user_form = Userform()
    property_form = PropertyForm()
    return render(request, 'Pro_add_Property.html', {'user_form': user_form, 'property_form': property_form})

def view_property_owner(request):
    property_owners = PropertyOwner.objects.all()
    return render(request, 'Pro_view__Property.html', {'property_owners': property_owners})



def edit_property_owner(request, id):
    property_owner = get_object_or_404(PropertyOwner, pk=id)

    if request.method == 'POST':
        user_form = Userform(request.POST, instance=property_owner.user)
        property_form = PropertyForm(request.POST, instance=property_owner)

        if user_form.is_valid() and property_form.is_valid():
            user_form.save()
            property_form.save()

            messages.success(request, 'Property owner updated successfully.')
            return redirect('view_property_owner')
        else:
            messages.error(request, 'Error updating property owner. Please check the form.')
            print(user_form.errors)
            print(property_form.errors)
    else:
        user_form = Userform(instance=property_owner.user)
        property_form = PropertyForm(instance=property_owner)

  
    return render(request, 'Pro_edit_Property.html', {'user_form': user_form, 'property_form': property_form})

def delete_property_owner(request, id):
    property_owner = get_object_or_404(PropertyOwner, pk=id)
    
    # Retrieve the associated user
    user_instance = property_owner.user
    print(user_instance)
    # Delete the property owner and associated user
    property_owner.delete()
    user_instance.delete()
    return redirect('view_property_owner')

def add_question(request):
    return render(request,'Chat_add_question.html')

def view_question(request):
    return render(request,'Chat_view_question.html')

def add_manage_property(request):
    return render(request,'Manage_add_Property.html')

def view_manage_property(request):
    property_owners = PropertyOwner.objects.all()
    return render(request,'Manage_view_Property.html', {'property_owners': property_owners})

def notification(request):
    return render(request,'Notification.html')

def privacy(request):
    # Assuming you have a model named TermsCondition with a field 'terms_condition'
    privacy = PrivacyPolicy.objects.all()

    if request.method == 'POST':
        privacy_policy_text = request.POST.get('privacy_policy', '')
        
        # Update or create the TermsCondition object
        obj, created = PrivacyPolicy.objects.update_or_create(defaults={'privacy_policy': privacy_policy_text})
        
        if created:
            messages.success(request, 'Insert Success')
        else:
            messages.success(request, 'Update Success')

        return redirect('privacy_policy')  # Redirect to the same page after form submission

    context = {
        'privacy': privacy,
    }

  
    return render(request,'privacy_policy.html',context)


def terms_condition(request):
    # Assuming you have a model named TermsCondition with a field 'terms_condition'
    terms_data = TermsCondition.objects.all()

    if request.method == 'POST':
        terms_condition_text = request.POST.get('terms_condition', '')
        
        # Update or create the TermsCondition object
        obj, created = TermsCondition.objects.update_or_create(defaults={'terms_condition': terms_condition_text})
        
        if created:
            messages.success(request, 'Insert Success')
        else:
            messages.success(request, 'Update Success')

        return redirect('terms_condition')  # Redirect to the same page after form submission

    context = {
        'terms_data': terms_data,
    }

    return render(request, 'terms_condition.html', context)


def profile(request):
    return render(request,'profile.html')



def manage_user_admin(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')

        if username and password:
            # Remove manual authentication check and login code
            return redirect('index')

    return render(request, 'Owner/login.html')

def index(request):
    return render(request,'Owner/index.html')


def delete_terms_condition(request, id):
    try:
        term = TermsCondition.objects.get(pk=id)
        term.delete()
        messages.success(request, 'Deleted Successfully')
    except TermsCondition.DoesNotExist:
        messages.error(request, 'Term not found')

    return redirect('terms_condition')


def delete_privacy_policy(request, id):
    try:
        privacy = PrivacyPolicy.objects.get(pk=id)
        privacy.delete()
        messages.success(request, 'Deleted Successfully')
    except PrivacyPolicy.DoesNotExist:
        messages.error(request, 'Privacy not found')

    return redirect('privacy_policy')