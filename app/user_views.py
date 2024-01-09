from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
import spacy
from gtts import gTTS
from fuzzywuzzy import fuzz
from spellchecker import SpellChecker
from fuzzywuzzy import process
from django. contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout, login as auth_login
from django.http import JsonResponse


@login_required(login_url='login_user')
def user_dashboard(request):
    return render(request,'user/user_dashboard.html')

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

           

            if user.user_type == '3':
                # Access and print user_session_id
                request.session['user_session_id'] = user.id
                user_session_id = request.session.get('user_session_id')
                print(f"User Session ID: {user_session_id}")

                return redirect('user_dashboard')  # User dashboard

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'user/login.html')



def logout_view_user(request):
   # Clear the session
    logout(request)

    # Optionally, you can delete the sessionid cookie
    response = redirect('login_user')
    response.delete_cookie('sessionid')  # Replace 'your_logout_redirect_view' with the actual logout redirect view
    return response

nlp = spacy.load("en_core_web_sm")

def get_answer_user(request):
    error_message = ''
    user_input = ''

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

                
                current_user = request.user

                
                user_room_number = get_object_or_404(Add_user, user=current_user).room_number

               
                matched_qa = QuestionAnswer.objects.filter(room=user_room_number, question__icontains=corrected_input).first()

                if not matched_qa:
                    questions = QuestionAnswer.objects.values_list('question', flat=True)
                    best_match, ratio = process.extractOne(corrected_input, questions)

                    if ratio >= 80:
                        matched_qa = QuestionAnswer.objects.filter(room=user_room_number, question=best_match).first()

                if matched_qa:
                    error_message = matched_qa.answer
                else:
                    error_message = 'Sorry, I don\'t have an answer for that question.'

                print('answer_text', error_message)

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

    return render(request, 'user/answer.html',
                  {'user_input': user_input, 'answer': error_message, 'audio_path': '/static/answer.mp3'})