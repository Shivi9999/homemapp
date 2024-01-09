from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django. contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout, login as auth_login
from django.http import JsonResponse
import spacy
from gtts import gTTS

from fuzzywuzzy import fuzz
from spellchecker import SpellChecker




@login_required(login_url='login_owner')
def owner_dashboard(request):
    room_count = Add_Room.objects.filter(flat_name__user=request.user).count()
    hotel_count = Add_hotel.objects.filter(user=request.user).count()
    user_count = Add_user.objects.filter(hotel_name__user=request.user).count()
    context={'room_count':room_count,'hotel_count':hotel_count,'user_count':user_count}
    return render(request,'Owner/index.html',context)

def login_owner(request):
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
                request.session['owner_session_id'] = user.id
                owner_session_id = request.session.get('owner_session_id')
                print(f"Owner Session ID: {owner_session_id}")

                return redirect('owner_dashboard')  # User dashboard

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Owner/login.html')



def logout_view_owner(request):
   # Clear the session
    logout(request)

    # Optionally, you can delete the sessionid cookie
    response = redirect('login_owner')
    response.delete_cookie('sessionid')  # Replace 'your_logout_redirect_view' with the actual logout redirect view
    return response






@login_required(login_url='login_owner')
def add_property_management(request):
    if request.method == 'POST':
        form = AddPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.user = request.user
            hotel.save()
            return redirect('view_property_management')
        else:
            print(form.errors)
            return render(request, 'Owner/Add_Property_management.html', {'form': form})
    else:
        form = AddPropertyForm()

    return render(request, 'Owner/Add_Property_management.html', {'form': form})


@login_required(login_url='login_owner')
def view_property_management(request):
    
    property_view = Add_hotel.objects.filter(user=request.user).order_by('-id')
   
    return render(request,'Owner/view_property_management.html',{'property_view':property_view})

@login_required(login_url='login_owner')
def edit_property(request, id):
    propertys = Add_hotel.objects.get(id=id)

    if request.method == 'POST':
        form = AddPropertyForm(request.POST, request.FILES, instance=propertys)
        if form.is_valid():
            form.save()
            return redirect('view_property_management')  # replace with your URL name
    else:
        form = AddPropertyForm(instance=propertys)

    return render(request, 'Owner/Edit_property.html', {'form': form, 'propertys': propertys})

@login_required(login_url='login_owner')
def delete_property(request, id):
    
    propertys = get_object_or_404(Add_hotel, id=id)
   
    propertys.delete()

   
    return JsonResponse({'msg': True})

@login_required(login_url='login_owner')
def add_room_management(request):
   
    if request.method == 'POST':
        form = AddRoomForm(request.user,request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_room_management')  # Assuming you have a URL pattern named 'room_list' for displaying the list of rooms
        else:
           print(form.errors )
    else:
        form = AddRoomForm(request.user)

   
    return render(request,'Owner/Room_Add_Management.html',{'form': form})

@login_required(login_url='login_owner')
def view_room_management(request):
    hotels = Add_hotel.objects.filter(user=request.user)
    
    # Fetch rooms associated with the hotels of the logged-in user
    room = Add_Room.objects.filter(flat_name__in=hotels)
   
    return render(request,'Owner/view_room_management.html',{'room':room})

@login_required(login_url='login_owner')
def edit_room(request, id):
    room = Add_Room.objects.get(id=id)

    if request.method == 'POST':
        form = AddRoomForm(request.user,request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('view_room_management')  # replace with your URL name
    else:
        form = AddRoomForm(request.user,instance=room)

    return render(request, 'Owner/edit_room.html', {'form': form, 'room': room})



@login_required(login_url='login_owner')
def delete_room(request,id):
    room = get_object_or_404(Add_Room, id=id)
    
    room.delete()
        

    return JsonResponse({'msg': True})



@login_required(login_url='login_owner')
def add_user_management(request):
    if request.method == "POST":
        form = Userform(request.POST)
        user_form= Add_userform(request.user,request.POST,request.FILES)
        
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
    user_form = Add_userform(request.user)
   
    return render(request,'Owner/user_management_add.html',{'form': form,'user_form': user_form})

@login_required(login_url='login_owner')    
def view_user_management(request):
    user_management=Add_user.objects.filter(hotel_name__user=request.user).order_by('-id')
    return render(request,'Owner/user_management_view.html',{'user_management':user_management})

@login_required(login_url='login_owner')
def edit_user(request, id):
    property_owner = get_object_or_404(Add_user, pk=id)

    if request.method == 'POST':
        user_form = Userform(request.POST, instance=property_owner.user)
        property_form = Add_userform(request.user,request.POST,request.FILES, instance=property_owner)

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
        property_form = Add_userform(request.user,instance=property_owner)

  
    return render(request, 'Owner/edit_user.html', {'user_form': user_form, 'property_form': property_form})

@login_required(login_url='login_owner')
def delete_user(request, id):
    user1 = get_object_or_404(Add_user, pk=id)
    
    # Retrieve the associated user
    user_instance = user1.user
    print(user_instance)
    # Delete the property owner and associated user
    user1.delete()
    user_instance.delete()
    return JsonResponse({'msg': True})



@login_required(login_url='login_owner')
def add_equipments(request):
   
    if request.method=="POST":
        equipment_form = property_equipment_form(request.POST)
        if equipment_form.is_valid():
            equipment=equipment_form.save(commit=False)
            equipment.save()
            return redirect('Add_equipment')
        else:
            print(equipment_form.errors)
            return render(request,'Owner/Add_equipment  .html',{'equipment_form':equipment_form})
    equipment_form=property_equipment_form(request.POST)
    equipment=PropertyAmenity.objects.all()      
    return render(request,'Owner/Add_equipment.html',{'equipment_form':equipment_form,'equipment':equipment})

@login_required(login_url='login_owner')
def view_equipments(request):
    user_hotels = Add_user.objects.filter(user=request.user)
    equipment = PropertyAmenity.objects.filter(add_user__in=user_hotels).order_by('-id')
    return render(request,'Owner/View_equipment.html',{'equipment':equipment})



@login_required(login_url='login_owner')
def edit_equipments(request, id):
    equipments = PropertyAmenity.objects.get(id=id)

    if request.method == 'POST':
        form = property_equipment_form(request.POST,instance=equipments)
        if form.is_valid():
            form.save()
            return redirect('Add_equipment')  # replace with your URL name
    else:
        form = property_equipment_form(instance=equipments)

    return render(request, 'Owner/Edit_equipments.html', {'form': form, 'equipments': equipments})

@login_required(login_url='login_owner')
def delete_equipments(request, id):
    equipments = get_object_or_404(PropertyAmenity, pk=id)
    
    # Retrieve the associated user
   
    equipments.delete()
    
    return JsonResponse({'msg': True})


@login_required(login_url='login_owner')    
def add_items(request):

    if request.method == 'POST':
        form = AddItemsForm(request.user,request.POST)
        if form.is_valid():
            # Save the form, associating it with the current user
            item_instance = form.save(commit=False)
            item_instance.user = request.user
            item_instance.save()
            return redirect('View_items')  # Replace 'item_list' with the URL name for your item list view
    else:
        form = AddItemsForm(request.user)

  
    return render(request,'Owner/add_items.html',{'form': form})

@login_required(login_url='login_owner')
def view_items(request):
    items=Add_items.objects.all().order_by('-id')
    return render(request,'Owner/view_items.html',{'items':items})


@login_required(login_url='login_owner')
def edit_items(request, id):
    items = Add_items.objects.get(id=id)

    if request.method == 'POST':
        form = AddItemsForm(request.user,request.POST,instance=items)
        if form.is_valid():
            form.save()
            return redirect('View_items')  # replace with your URL name
    else:
        form = AddItemsForm(request.user,instance=items)

    return render(request, 'Owner/Edit_items.html', {'form': form, 'items': items})


@login_required(login_url='login_owner')
def delete_items(request, id):
    items = get_object_or_404(Add_items, pk=id)
    
    # Retrieve the associated user
   
    items.delete()
    
    return JsonResponse({'msg': True})

@login_required(login_url='login_owner')
def get_rooms(request):
    if request.method == 'POST':
        try:
            selected_hotel_ids = request.POST.getlist('hotel_ids[]')
            rooms = Add_Room.objects.filter(flat_name_id__in=selected_hotel_ids)

            rooms_data = [{'id': room.id, 'room_number': room.room_number} for room in rooms]
            return JsonResponse({'rooms': rooms_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='login_owner')
def Add_question_answer(request):
    if request.method=="POST":
            chat_form = QuestionForm(request.POST)
            if chat_form.is_valid():
                chat=chat_form.save(commit=False)
                chat.save()
                return redirect('View_question_answer')
            else:
                print(chat_form.errors)
                return render(request,'Owner/question_answer.html',{'chat_form':chat_form})
    chat_form=QuestionForm(request.POST)
         
    return render(request,'Owner/question_answer.html',{'chat_form':chat_form})


@login_required(login_url='login_owner')
def view_question_answer(request):
    hotels = Add_hotel.objects.filter(user=request.user)
    
    # Fetch questions associated with the hotels of the logged-in user
    chat = QuestionAnswer.objects.filter(hotel__in=hotels)
      
    return render(request, 'Owner/que_ans_view.html', {'chat': chat})


@login_required(login_url='login_owner')
def edit_question_answer(request,id):
    quetion_ins = get_object_or_404(QuestionAnswer, pk=id)
    if request.method == "POST":
        question_form = QuestionForm(request.POST,instance=quetion_ins)
       
        if question_form.is_valid():
      
            owner_instance = question_form.save(commit=False)
            
            owner_instance.save()
            
            return redirect('View_question_answer')
        else:
            print(question_form.errors)
      
    else:
     question_form = QuestionForm(instance=quetion_ins)
    return render(request,'Owner/edit_question_answer.html',{'question_form':question_form})


@csrf_protect
@login_required(login_url='login_owner')
def delete_question_answer(request, id):
    
    question = get_object_or_404(QuestionAnswer, id=id)
   
    question.delete()

   
    return JsonResponse({'msg': True})
    

@login_required(login_url='login_owner')
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

@login_required(login_url='login_owner')
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



@login_required(login_url='login_owner')
def delete_faq(request, id):
    
    
    faq = get_object_or_404(Faq, pk=id)
  
    faq.delete()
    
    return JsonResponse({'msg': True})


@login_required(login_url='login_owner')
def Notification_owner1(request):
    if request.method == 'POST':
        form = OwnerNotificationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            instance.users.add(request.user)  # Associate the notification with the logged-in user
            form.save_m2m()
            return redirect('Notification_owner')
        else:
            print(form.errors)
    else:
        form = OwnerNotificationForm()
        user_hotel = Add_hotel.objects.get(user=request.user)

        # Fetch notifications associated with the hotel of the logged-in owner
        notifications = Notification_owner.objects.all()


        print(user_hotel)  # Make sure user_hotel is not None
        print(notifications)  # Check if notifications are fetched
        return render(request, 'Owner/Notification.html', {'form': form, 'notifications': notifications})

       


@login_required(login_url='login_owner')
def edit_notification_owner(request, id):
    notification_owner = get_object_or_404(Notification_owner, id=id)

    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification_owner)
        if form.is_valid():
            form.save()
            return redirect('Notification_owner')  
    else:
        form = NotificationForm(instance=notification_owner)

    return render(request, 'Owner/Edit_notification.html', {'form': form, 'notification_owner': notification_owner})

@login_required(login_url='login_owner')
def delete_notification_owner(request,id):
    notification_owner = get_object_or_404(Notification_owner, id=id)
   
    notification_owner.delete()
      

    return JsonResponse({'msg': True})  




@login_required(login_url='login_owner')
def profile_owner(request):
    # Retrieve the PropertyOwner instance related to the logged-in user
    owner_profile = get_object_or_404(PropertyOwner, user=request.user)

    profile_form = Userform(instance=request.user)
    owner_form = PropertyForm(instance=owner_profile)

    form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'Owner/profile.html', {'profile_form': profile_form, 'form': form, 'owner_form': owner_form})


@login_required(login_url='login_owner')
def update_personal_details_owner(request):
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

    return redirect('Profile_owner')


@login_required(login_url='login_owner')
def change_password_owner(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
        else:
            print(form.errors)
            messages.error(request, 'Error changing password. Please check the form.')
            return render(request,'Owner/profile.html',{'form':form})

    return redirect('Profile_owner')

@login_required(login_url='login_owner')
def terms_condition_owner(request):
    terms_data = TermsCondition.objects.all()
    return render(request,'Owner/terms_condition.html',{'terms_data':terms_data})

@login_required(login_url='login_owner')
def privacy_policy_owner(request):
    fetch_privacy=PrivacyPolicy.objects.all()
    return render(request,'Owner/privacy_policy.html',{'fetch_privacy':fetch_privacy})



@login_required(login_url='login_owner')
def owner_chat(request):
    return render(request,'Owner/chating.html')

nlp = spacy.load("en_core_web_sm")
   

@login_required(login_url='login')  # Assuming you have a login view with the name 'login'
def get_answer_owner(request):
    error_message = ''
    user_input = ''
    user_qas = None 

    try:
        if request.method == 'GET':
            user_input = request.GET.get('user_input', '').lower().strip()

            if not user_input:
                error_message = 'Please provide a question.'
            else:
                spell_checker = SpellChecker()
                corrected_input = ' '.join(spell_checker.correction(word) for word in user_input.split())
                nlp = spacy.load("en_core_web_sm")
                input_doc = nlp(corrected_input)

                
                user_hotels = Add_hotel.objects.filter(user=request.user)
                user_qas = QuestionAnswer.objects.filter(hotel__in=user_hotels)


                matched_qa = user_qas.filter(question__icontains=corrected_input).first()
                if not matched_qa:
                    questions = user_qas.values_list('question', flat=True)
                    best_match, ratio = process.extractOne(corrected_input, questions)

                    if ratio >= 80:
                        matched_qa = user_qas.filter(question=best_match).first()

                if matched_qa:
                    error_message = matched_qa.answer
                else:
                    error_message = 'Sorry, I don\'t have an answer for that question.'

        else:
            error_message = 'Invalid request method.'

    except Exception as e:
        error_message = 'Sorry, an error occurred.'
        print(f"An error occurred: {str(e)}")

    finally:
        if not error_message:
            error_message = 'Sorry, an error occurred.'

        tts = gTTS(text=error_message, lang='en')
        tts.save("static/answer.mp3")

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'answer': error_message, 'audio_path': '/static/answer.mp3'}, safe=False)

    return render(request, 'Owner/answer.html',
                  {'user_input': user_input, 'answer': error_message, 'audio_path': '/static/answer.mp3',
                   'user_hotels': user_hotels, 'user_qas': user_qas})