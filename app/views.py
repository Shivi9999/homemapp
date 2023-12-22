from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import os
from gtts import gTTS
import pyttsx3

from django.conf import settings
import spacy
from fuzzywuzzy import fuzz
from spellchecker import SpellChecker
from fuzzywuzzy import process
from django. contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd 
# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    property_owner_count=PropertyOwner.objects.all().count()
    question_count=QuestionAnswer.objects.all().count()
   
    context={'property_owner_count':property_owner_count,'question_count':question_count}
    return render(request,'index.html',context)


# KIGGGGGGGGG

def login(request):
    # Print the entire session dictionary
    print(request.session)

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
           

            if user.user_type == '1':
                # Access and print admin_session_id
                request.session['admin_session_id'] = user.id
                admin_session_id = request.session.get('admin_session_id')
                print(f"Admin Session ID: {admin_session_id}")

                return redirect('dashboard')  # Admin dashboard

           

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')



def logout_view(request):
   # Clear the session
    logout(request)

    # Optionally, you can delete the sessionid cookie
    response = redirect('login')
    response.delete_cookie('sessionid')  # Replace 'your_logout_redirect_view' with the actual logout redirect view
    return response



@login_required(login_url='login')
def add_property_owner(request):
    if request.method == "POST":
        user_form = Userform(request.POST)
        property_form = PropertyForm(request.POST)
        
        if user_form.is_valid() and property_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            
            print("Form Data:", user_form.cleaned_data)
            user_form.instance.user_type = '2'
            print()
            user_instance = user_form.save(commit=False)
            # Set the user type statically
            user_instance.set_password(password)
            user_instance.save()
            saved_user = User.objects.get(pk=user_instance.pk)
            print("Saved User Type:", saved_user.user_type)
            owner_instance = property_form.save(commit=False)
            owner_instance.user = user_instance
            owner_instance.save()
            
            return redirect('View_property_owner')
        else:
            print(user_form.errors)
            print(property_form.errors)
            return render(request, 'Pro_add_Property.html', {'user_form': user_form, 'property_form': property_form})

    user_form = Userform()
    property_form = PropertyForm()
    return render(request, 'Pro_add_Property.html', {'user_form': user_form, 'property_form': property_form})

@login_required(login_url='login')
def view_property_owner(request):
    property_owners = PropertyOwner.objects.all().order_by('-id')
    return render(request, 'Pro_view__Property.html', {'property_owners': property_owners})




def forget_password(request):
   
    return render(request, 'forget_pass.html')


@login_required(login_url='login')
def edit_property_owner(request, id):
    property_owner = get_object_or_404(PropertyOwner, pk=id)

    if request.method == 'POST':
        user_form = Userform(request.POST, instance=property_owner.user)
        property_form = PropertyForm(request.POST, instance=property_owner)

        if user_form.is_valid() and property_form.is_valid():
            user_form.save()
            property_form.save()

            messages.success(request, 'Property owner updated successfully.')
            return redirect('View_property_owner')
        else:
            messages.error(request, 'Error updating property owner. Please check the form.')
            print(user_form.errors)
            print(property_form.errors)
            return render(request, 'Pro_edit_Property.html', {'user_form': user_form, 'property_form': property_form})
    else:
        user_form = Userform(instance=property_owner.user)
        property_form = PropertyForm(instance=property_owner)

  
    return render(request, 'Pro_edit_Property.html', {'user_form': user_form, 'property_form': property_form})

@login_required(login_url='login')
def delete_property_owner(request, id):
    property_owner = get_object_or_404(PropertyOwner, pk=id)
    
    # Retrieve the associated user
    user_instance = property_owner.user
    print(user_instance)
    # Delete the property owner and associated user
    property_owner.delete()
    user_instance.delete()
    
    return JsonResponse({'msg': True})


@login_required(login_url='login')
def add_question(request):
    
    question_form = QuestionForm()
    return render(request,'Chat_add_question.html',{'question_form':question_form})

@login_required(login_url='login')
def view_question(request):
    que_ans=QuestionAnswer.objects.all().order_by('-id')
    return render(request,'Chat_view_question.html',{'que_ans':que_ans})


@login_required(login_url='login')
def edit_question(request,id):
    quetion_ins = get_object_or_404(QuestionAnswer, pk=id)
    if request.method == "POST":
        question_form = QuestionForm(request.POST,instance=quetion_ins)
       
        if question_form.is_valid():
      
            owner_instance = question_form.save(commit=False)
            
            owner_instance.save()
            
            return redirect('View_question')
        else:
            print(question_form.errors)
      
    else:
     question_form = QuestionForm(instance=quetion_ins)
    return render(request,'edit_question_answer.html',{'question_form':question_form})


@csrf_protect
@login_required(login_url='login')
def delete_question(request, id):
    
    question = get_object_or_404(QuestionAnswer, id=id)
   
    question.delete()

   
    return JsonResponse({'msg': True})
    
# def delete_question(request, id):
#     question_answer = get_object_or_404(QuestionAnswer, pk=id)
#      # Delete the property owner and associated user
#     question_answer.delete()
    
#     return redirect('View_question')

@login_required(login_url='login')
def add_manage_property(request):
    return render(request,'Manage_add_Property.html')

@login_required(login_url='login')
def view_manage_property(request):
    property_owners = PropertyOwner.objects.all().order_by('-id')
    return render(request,'Manage_view_Property.html', {'property_owners': property_owners})


# @login_required(login_url='login')
# def notification(request):
#     return render(request,'Notification.html')


@login_required(login_url='login')
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

        return redirect('Privacy_Policy')  # Redirect to the same page after form submission

    context = {
        'privacy': privacy,
    }

  
    return render(request,'privacy_policy.html',context)


@login_required(login_url='login')
def notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()  # Save the many-to-many relationships
           
            return redirect('notification')
        else:
            print(form.errors)
    else:
        form = NotificationForm()

    notifications = Notification.objects.all()
    return render(request, 'Notification.html', {'form': form, 'notifications': notifications})

# @login_required(login_url='login')
# def notification(request):
   
#     if request.method == 'POST':
#         form = NotificationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('notification')  # Redirect to a confirmation page or another URL
#         else:
#             print(form.errors)
#     else:
#         form = NotificationForm()
#     notifications=Notification.objects.all()
#     return render(request, 'Notification.html', {'form': form,'notifications':notifications})




@login_required(login_url='login')
def edit_notification(request, id):
    notification = get_object_or_404(Notification, id=id)

    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            return redirect('notification')  # Redirect to the notification list view
    else:
        form = NotificationForm(instance=notification)

    return render(request, 'edit_notification.html', {'form': form, 'notification': notification})

@login_required(login_url='login')
def delete_notification(request,id):
    notification = get_object_or_404(Notification, id=id)
   
    notification.delete()
      

    return JsonResponse({'msg': True})  # Redirect to the notification list view


@login_required(login_url='login')
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


# def profile(request):
#     if request.method == 'POST':
#         form = CustomPasswordChangeForm(request.user, request.POST)
#         profile_form = Userform(request.POST)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('profile')  # Redirect to the profile page or wherever you want
#         else:
#             print(form.errors)

#         if profile_form.is_valid():
#             # Update user profile data
#             request.user.username = profile_form.cleaned_data['username']
#             request.user.email = profile_form.cleaned_data['email']
#             request.user.password = profile_form.cleaned_data['password']
#             request.user.save()
#             messages.success(request, 'Your profile was successfully updated!')
#             return redirect('profile')  # Redirect to the profile page or wherever you want
#         else:
#             print(profile_form.errors)
#     else:
#         form = CustomPasswordChangeForm(request.user)
#         profile_form = Userform(initial={'username': request.user.username, 'email': request.user.email,'password': request.user.password})
#     return render(request,'profile.html', {'form': form,'profile_form':profile_form})


@login_required(login_url='login')
def profile(request):
    profile_form = Userform(instance=request.user)
    form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'profile.html', {'profile_form': profile_form,'form':form})



def manage_user_admin(request):
   
    if request.method == 'GET' and 'email' in request.GET and 'password' in request.GET:
        email = request.GET['email']
        password = request.GET['password']
        print('email',email)

        print('password',password)
        user = User.objects.get(email=email, password=password)
        print('user',user)
        if user is not None:
            auth_login(request, user)
            return redirect('user_dashboard')  # Redirect to your dashboard
        else:
            messages.error(request, 'Email or Password is invalid.')

    return render(request, 'login.html')  # Render your template with the appropriate context


def index(request):
    return render(request,'Owner/index.html')

@login_required(login_url='login')
def delete_terms_condition(request, id):
    terms_condition = get_object_or_404(TermsCondition, id=id)
   
    terms_condition.delete()

    return JsonResponse({'msg': True})


@login_required(login_url='login')
def delete_privacy_policy(request, id):
    privacy = get_object_or_404(PrivacyPolicy, id=id)
   
    privacy.delete()

    return JsonResponse({'msg': True})


# def import_data(request):
#     return render(request,'Notification.html')




@login_required(login_url='login')
def update_personal_details(request):
    if request.method == 'POST':
        form = Userform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal details updated successfully!')
        else:
            messages.error(request, 'Error updating personal details. Please check the form.')

    return redirect('profile')



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
        else:
            messages.error(request, 'Error changing password. Please check the form.')

    return redirect('profile')


# @login_required(login_url='login')
# def update_profile_picture(request):
#     if request.method == 'POST':
#         form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile picture updated successfully!')
#         else:
#             messages.error(request, 'Error updating profile picture. Please check the form.')

#     return redirect('profile')


@login_required(login_url='login')
def save_question_answer(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)

        if question_form.is_valid():
            question_form.save()
         
            
            return redirect('View_question')
        else:
            errors = question_form.errors
            return render(request, 'Chat_add_question.html', {'question_form': question_form, 'errors': errors})
    return redirect('add_question')  

# def process_and_save_excel_data(excel_file):
#     # Assuming your Excel file has columns named 'question' and 'answer'
#     df = pd.read_excel(excel_file)
    
#     # Iterate over rows and save data to QuestionAnswer model
#     for index, row in df.iterrows():
#         question_text = row['question']
#         answer_text = row['answer']
        
#         # Save data to the model
#         question_answer = QuestionAnswer(question=question_text, answer=answer_text)
#         question_answer.save()

# @login_required(login_url='login')
# def import_excel(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['excel_file']
#             process_and_save_excel_data(excel_file)

#             messages.success(request, 'Excel file imported and data saved successfully!')
#         else:
#             messages.error(request, 'Error importing Excel file. Please check the form and try again.')
#     else:
       

#     return redirect('add_question')

# @login_required(login_url='login')
# def delete_user(request):
#     user_id = request.POST.get('userID')

#     # Perform user deletion logic here

#     # For example, you can delete the user and return a success message
#     response_data = {'msg': True}
#     return JsonResponse(response_data)

############################## CHAT #############################################

@login_required(login_url='login')
def chat(request):
    return render(request,'chatbot/index.html')
    


@login_required(login_url='login')
def get_answer(request):
    try:
        if request.method == 'GET':
            user_input = request.GET.get('user_input', '').lower().strip()

            if not user_input:
                return JsonResponse({'answer': 'Please provide a question.'})

            # Spell-check user input
            spell_checker = SpellChecker()
            corrected_input = ' '.join(spell_checker.correction(word) for word in user_input.split())
            nlp = spacy.load("en_core_web_sm")
            input_doc = nlp(corrected_input)

            matched_qa = QuestionAnswer.objects.filter(question__icontains=corrected_input).first()
            if not matched_qa:
                # If an exact match is not found, try fuzzy matching
                questions = QuestionAnswer.objects.values_list('question', flat=True)
                best_match, ratio = process.extractOne(corrected_input, questions)

                if ratio >= 80:
                    matched_qa = QuestionAnswer.objects.filter(question=best_match).first()

            # Generate speech from the answer or "Sorry" message with pyttsx3
            if matched_qa:
                answer_text = matched_qa.answer
            else:
                answer_text = 'Sorry, I don\'t have an answer for that question.'
 
            print('answer_text', answer_text)

            try:
                            # Initialize the text-to-speech engine
                            engine = pyttsx3.init()

                            # Set properties (optional)
                            engine.setProperty('rate', 150)  # Adjust the speed as needed

                            # Use pyttsx3 to directly speak the answer
                            engine.say(answer_text)

                            # Log statements to check the control flow
                            print("Before engine.runAndWait()")
                            engine.runAndWait()
                            print("After engine.runAndWait()")

            except Exception as e:
                            print(f"An error occurred during TTS: {str(e)}")


            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                print('answer', answer_text)
                return JsonResponse({'answer': answer_text}, safe=False)

            return render(request, 'chatbot/answer.html',
                          {'user_input': user_input, 'answer': answer_text})
            

        else:
            return JsonResponse({'error': 'Invalid request method.'})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'Sorry, I don\'t have an answer for that question.'})


def import_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl')
                else:
                    raise ValueError('Unsupported file format. Please upload a CSV or Excel file.')
                
                for _, row in df.iterrows():
                    question = row['question']
                    answer = row['answer']
                    QuestionAnswer.objects.create(question=question, answer=answer)
                
                messages.success(request, 'File imported successfully.')
            except Exception as e:
                messages.error(request, f'Error importing file: {str(e)}')
            
            return redirect('import_csv')  # Redirect to the same page after import

    else:
        form = CSVUploadForm()

    return render(request, 'kil.html', {'form': form})


