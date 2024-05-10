import json
import logging
import random

import nltk
import openai
import pandas as pd
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from SurveyAiApp.models import Answer, Question, UserSurvey

# from SurveyAiApp.models import customerSatisfaction1


logger = logging.getLogger(__name__)



#from SurveyAiApp.models import SurveyResponse


def calculate_sentiment_percentage(request):
    return HttpResponse("Page Under Creation");




def home(request):
    return render(request, 'index.html')

def build_AI(request):
    return render(request, 'buildwith_ai.html')

def register(request):
    return render(request, 'register.html')

def generate_healthcare_questions(num_questions=10):
    healthcare_keywords = ['health', 'care', 'medicine', 'hospital', 'doctor', 'patient', 'treatment', 'wellness', 'disease']
    questions = []
    for i in range(1, num_questions + 1):
        question_type = random.choice(['multiple_choice', 'dropdown', 'rating_scale', 'paragraph'])
        if question_type == 'multiple_choice':
            options = random.sample(healthcare_keywords, 3)
            correct_answer = random.choice(options)
            question = "What is the most important aspect of healthcare among {}?".format(', '.join(options))
        elif question_type == 'dropdown':
            question = "Select the most important aspect of healthcare among:"
            options = healthcare_keywords.copy()
            random.shuffle(options)
        elif question_type == 'rating_scale':
            question = "On a scale of 1 to 5, how important is {} in healthcare?".format(random.choice(healthcare_keywords))
            options = list(range(1, 6))
        elif question_type == 'paragraph':
            question = "Please describe your experience with healthcare:"
            options = None  
        questions.append({'question_number': i, 'question_type': question_type, 'question_text': question, 'options': options})
    return questions

def generate_healthcare_questions_json(request):
    num_questions = request.GET.get('num_questions', 10)
    try:
        num_questions = int(num_questions)
    except ValueError:
        num_questions = 10 
    healthcare_questions = generate_healthcare_questions(num_questions)
    json_data = json.dumps({'healthcare_questions': healthcare_questions})
    #return render(request, 'src/AI_preview.html', {'healthcare_questions': healthcare_questions})
    #return render(request, 'healthcare_questions01.html', {'healthcare_questions': healthcare_questions})
    return JsonResponse(json_data, safe=False)

def generate_hospitality_travel_questions(num_questions=10):
    hospitality_travel_keywords = ['hotel', 'accommodation', 'travel', 'destination', 'tourism', 'resort', 'flight', 'beach', 'sightseeing']
    questions = []
    for i in range(1, num_questions + 1):
        question_type = random.choice(['multiple_choice', 'dropdown', 'rating_scale', 'paragraph'])
        if question_type == 'multiple_choice':
            options = random.sample(hospitality_travel_keywords, 3)
            correct_answer = random.choice(options)
            question = "What is the most important aspect of hospitality and travel among {}?".format(', '.join(options))
        elif question_type == 'dropdown':
            question = "Select the most important aspect of hospitality and travel among:"
            options = hospitality_travel_keywords.copy()
            random.shuffle(options)
        elif question_type == 'rating_scale':
            question = "On a scale of 1 to 5, how important is {} in hospitality and travel?".format(random.choice(hospitality_travel_keywords))
            options = list(range(1, 6))
        elif question_type == 'paragraph':
            question = "Please describe your experience with hospitality and travel:"
            options = None 
        questions.append({'question_number': i, 'question_type': question_type, 'question_text': question, 'options': options})
    return questions    

def generate_hospitality_travel_json(request):
    num_questions = request.GET.get('num_questions', 10)
    try:
        num_questions = int(num_questions)
    except ValueError:
        num_questions = 10 
    hospitality_travel_questions = generate_hospitality_travel_questions(num_questions)
    json_data = json.dumps({'hospitality_travel_questions': hospitality_travel_questions})
    #return render(request, 'hospitality_travel_questions.html', {'hospitality_travel_questions': hospitality_travel_questions})
    return JsonResponse(json_data, safe=False)


def store_healthcare_answers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        healthcare_responses = data.get('healthcare_responses', [])
        for response in healthcare_responses:
            question_number = response.get('question_number')
            question_type = response.get('question_type')
            response_text = response.get('response')
            SurveyResponse.objects.create(
                question_number=question_number,
                question_type=question_type,
                response=response_text
            )
        return HttpResponse("Responses stored successfully!", status=200)
    else:
        return HttpResponse("Invalid request method", status=400)

def store_hospitality_travel_answers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        hospitality_travel_responses = data.get('hospitality_travel_responses', [])
        for response in hospitality_travel_responses:
            question_number = response.get('question_number')
            question_type = response.get('question_type')
            response_text = response.get('response')
            SurveyResponse.objects.create(
                question_number=question_number,
                question_type=question_type,
                response=response_text
            )
        return HttpResponse("Responses stored successfully!", status=200)
    else:
        return HttpResponse("Invalid request method", status=400)

def generate_education_questions(num_questions=10):
    education_keywords = ['education', 'school', 'learning', 'students', 'teachers', 'curriculum', 'college', 'university', 'classroom']
    questions = []
    for i in range(1, num_questions + 1):
        question_type = random.choice(['multiple_choice', 'dropdown', 'rating_scale', 'paragraph'])
        if question_type == 'multiple_choice':
            options = random.sample(education_keywords, 3)
            correct_answer = random.choice(options)
            question = "What is the most important aspect of education among {}?".format(', '.join(options))
        elif question_type == 'dropdown':
            question = "Select the most important aspect of education among:"
            options = education_keywords.copy()
            random.shuffle(options)
        elif question_type == 'rating_scale':
            question = "On a scale of 1 to 5, how important is {} in education?".format(random.choice(education_keywords))
            options = list(range(1, 6))
        elif question_type == 'paragraph':
            question = "Please describe your experience with education:"
            options = None  # No predefined options for paragraph type
        questions.append({'question_number': i, 'question_type': question_type, 'question_text': question, 'options': options})
    return questions

def generate_education_questions_json(request):
    num_questions = request.GET.get('num_questions', 10)
    try:
        num_questions = int(num_questions)
    except ValueError:
        num_questions = 10 
    education_questions = generate_education_questions(num_questions)
    json_data = json.dumps({'education_questions': education_questions})
    #return render(request, 'education_questions.html', {'education_questions': education_questions})
    return JsonResponse({'education_questions': education_questions},safe=False)    

def generate_employee_satisfaction_questions(num_questions=10):
    employee_satisfaction_keywords = ['job', 'workplace', 'colleagues', 'management', 'benefits', 'culture', 'communication', 'growth', 'recognition']
    questions = []
    for i in range(1, num_questions + 1):
        question_type = random.choice(['multiple_choice', 'dropdown', 'rating_scale', 'paragraph'])
        if question_type == 'multiple_choice':
            options = random.sample(employee_satisfaction_keywords, 3)
            correct_answer = random.choice(options)
            question = "What is the most important aspect of employee satisfaction among {}?".format(', '.join(options))
        elif question_type == 'dropdown':
            question = "Select the most important aspect of employee satisfaction among:"
            options = employee_satisfaction_keywords.copy()
            random.shuffle(options)
        elif question_type == 'rating_scale':
            question = "On a scale of 1 to 5, how satisfied are you with {} in your workplace?".format(random.choice(employee_satisfaction_keywords))
            options = list(range(1, 6))
        elif question_type == 'paragraph':
            question = "Please describe your overall satisfaction with your current job:"
            options = None  # No predefined options for paragraph type
        questions.append({'question_number': i, 'question_type': question_type, 'question_text': question, 'options': options})
    return questions

def generate_employee_satisfaction_questions_json(request):
    num_questions = request.GET.get('num_questions', 10)
    try:
        num_questions = int(num_questions)
    except ValueError:
        num_questions = 10 
    employee_satisfaction_questions = generate_employee_satisfaction_questions(num_questions)
    json_data = json.dumps({'employee_satisfaction_questions': employee_satisfaction_questions})
    return render(request, 'employee_satisfaction_questions.html', {'employee_satisfaction_questions': employee_satisfaction_questions})
   # return JsonResponse({'employee_satisfaction_questions': employee_satisfaction_questions},safe=False)

def store_employee_satisfaction_answers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        employee_satisfaction_responses = data.get('employee_satisfaction_responses', [])
        for response in employee_satisfaction_responses:
            question_number = response.get('question_number')
            question_type = response.get('question_type')
            response_text = response.get('response')
            SurveyResponse.objects.create(
                question_number=question_number,
                question_type=question_type,
                response=response_text
            )
        return HttpResponse("Responses stored successfully!", status=200)
    else:
        return HttpResponse("Invalid request method", status=400)

def survey_view(request):
    if request.method == 'POST':
        
        topic = request.POST.get('topic')

        api_url = f'sk-nxsvhnnwkw3ph2iutkyzt3blbkfj7ytjjjpn8kt3yhy2xr1e/?topic={topic}'

        response = requests.get(api_url)
        
        if response.status_code == 200:
            questions = response.json()['questions']
            #return render(request, 'survey_template.html', {'questions': questions})
            return JsonResponse({'questions': questions},safe=False)
        else:
            error_message = "Error retrieving survey questions"
            return render(request, 'error_template.html', {'error_message': error_message})
    return render(request, 'topic_input_form.html')
        
def chat_with_gpt(message):
    
    prompt = "Your dynamic prompt here: " + message
    
    print("Dynamic prompt:", prompt)
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=1.0
    )
    
    return response.choices[0].text.strip()

def maintence(request):
    return render(request, 'maintenece.html')



def chat_with_gpt_view(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        response = chat_with_gpt(message)
        
        survey_question = SurveyQuestion.objects.create(
            question=message,
            response=response
        )
        survey_question.save()

        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Method not Allowed'}, status=405)

def my_view_function(request):
    if request.method == 'GET':
        survey_input = request.GET.get('survey_input', '')
        message = survey_input
        # message="Who is Srk"
        response_from_ai = chat_with_gpt(message)
        return JsonResponse({'input':survey_input,'response_from_ai': response_from_ai})
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405) 

def starter_temp(request):
    return render (request, 'Start_from_template.html')

def healthcarequestions(request):
    questions = Question.objects.filter(tag='healthcare')
    context = {'questions': questions}

    if request.method == "POST":
        username = request.POST["username"]
        for i in request.POST:
            if i not in ("username", "csrfmiddlewaretoken"):
                if i.startswith("m-"):
                    answers = request.POST.getlist(i)
                    for ans in answers:
                        UserSurvey.objects.create(user_name=username, question_id=i.replace("m-", ""), answer=ans)
                else:
                    answer = request.POST.get(i)
                    UserSurvey.objects.create(user_name=username, question_id=i.replace("d-", ""), answer=answer)

        #return render(request, 'Survey_preview.html', context=context)
    return render(request, 'preview_template_survey.html', context=context)
    #return HttpResponse("Helllo")
    #return render(request,'Survey_preview.html')

def buildWithScratch(request):
    return render(request, 'Build_Scratch.html')   

def buildwithAi(request):
    return render(request, 'Build_withAI.html')

def ai_preview(request):
    return render(request,'AI_preview.html')

def startFromTemplate(request):
    return render(request, 'buildwith_template.html')

def customer_satisfaction(request):
    questions = Question.objects.filter(tag='customer')
    context = {'questions': questions}

    if request.method == "POST":
        username = request.POST["username"]
        for i in request.POST:
            if i not in ("username", "csrfmiddlewaretoken"):
                if i.startswith("m-"):
                    answers = request.POST.getlist(i)
                    for ans in answers:
                        UserSurvey.objects.create(user_name=username, question_id=i.replace("m-", ""), answer=ans)
                else:
                    answer = request.POST.get(i)
                    UserSurvey.objects.create(user_name=username, question_id=i.replace("d-", ""), answer=answer)

        # return render(request, 'customer_satisfaction_2.html', context=context)
    
    return render(request, 'preview_template_survey.html', context=context)
           #return render(request, 'Customer_satisfaction.html')

def universityinstructor(request):
    questions = Question.objects.filter(tag='universityinstructor')
    context = {'questions': questions}

    if request.method == "POST":
        username = request.POST["username"]
        for i in request.POST:
            if i not in ("username", "csrfmiddlewaretoken"):
                if i.startswith("m-"):
                    answers = request.POST.getlist(i)
                    for ans in answers:
                        UserSurvey.objects.create(user_name=username, question_id=i.replace("m-", ""), answer=ans)
                else:
                    answer = request.POST.get(i)
                    UserSurvey.objects.create(user_name=username, question_id=i.replace("d-", ""), answer=answer)

        
    return render(request, 'preview_template_survey.html', context=context)
    #return render(request, 'universityinstructor.html')

def eventfeedback(request):
    return render(request, 'EventFeedback.html')

def softwarefeedback(request):
    return render(request, 'SoftwareFeedback.html') 
def retailsurvey(request):
    return render(request, 'RetailSurvey.html')   

def volunteerfeedback(request):
    return render(request, 'VolunteerFeedback.html')

def workfromhome(request):
    return render(request, 'WorkFromHome.html')

def netpromotor(request):
    return render(request, 'NetPromotor.html')
def customerservice(request):
    return render(request, 'CustomerService.html')
def applicationexperience(request):
    return render(request,'ApplicationExperience.html')  
def businesstobusiness(request):
    return render(request,'BusinessToBusiness.html')  
def brandawareness(request):
    return render(request, 'Brandawareness.html')
def emailnewsletter(request):
    return render(request,'EmailNewsLetter.html')
def employeeawardnomination(request):
    return render(request, 'EmployeeAwardNomination.html')

def competitivedifferentiation(request):
    return render(request, 'CompetitiveDifferentiation.html')   

def customerimpactsurvey(request):
    return render(request,'CustomerImpactSurvey.html')

def generalhighschoolsatisfaction(request):
    return render(request,'GeneralHighSchoolSatisfaction.html')

def k12parentsurvey(request):
    return render(request,'k12ParentSurvey.html')
def k12distancelearning(request):
    return render(request,'k12DistanceLearning.html') 

def quiz(request):
    return render(request,'Quiz.html')       

def quiz01(request):
    return render(request,'Quiz01.html')

def alumni(request):
    return render(request, 'Alumni.html')

def endurance(request):
    return render(request, 'Endurance.html')
def eventplanning(request):
    return render(request,'EventPlanning.html')    

import random


def save_healthcare_questions(num_questions=10):
    healthcare_keywords = ['health', 'care', 'medicine', 'hospital', 'doctor', 'patient', 'treatment', 'wellness', 'disease']
    for i in range(1, num_questions + 1):
        question_type = random.choice(['multiple_choice', 'dropdown', 'rating_scale', 'paragraph'])
        if question_type == 'multiple_choice':
            options = random.sample(healthcare_keywords, 3)
            correct_answer = random.choice(options)
            question_text = "What is the most important aspect of healthcare among {}?".format(', '.join(options))
        elif question_type == 'dropdown':
            question_text = "Select the most important aspect of healthcare among:"
            options = healthcare_keywords.copy()
            random.shuffle(options)
        elif question_type == 'rating_scale':
            question_text = "On a scale of 1 to 5, how important is {} in healthcare?".format(random.choice(healthcare_keywords))
            options = list(range(1, 6))
        elif question_type == 'paragraph':
            question_text = "Please describe your experience with healthcare:"
            options = None
        HealthcareQuestion.objects.create(
            question_number=i,
            question_type=question_type,
            question_text=question_text,
            options=options
        )

# def submit_survey_responses(request):
#     if request.method == 'POST':
#         # Get the survey response data from the POST request
#         response_data = request.POST
        
#         # Loop through the response data and save each response to the database
#         for key, value in response_data.items():
#             # Extract the question number from the key
#             question_number = key.split('_')[1]

#             # Check if the question is a paragraph-based question
#             if key.startswith('question') and not key.endswith('_'):
#                 question_type = 'paragraph'
#             else:
#                 question_type = 'multiple_choice' if key.startswith('question') else 'dropdown'

#             # For customer satisfaction questions, save the responses to the customerSatisfaction model
#             if question_type != 'paragraph':
#                 try:
#                     # Use the model manager to query the customerSatisfaction object
#                     question_text = customerSatisfaction1.objects.get(question_number=question_number).question_text
#                     answer = value
#                     satisfaction_response = customerSatisfaction1(
#                         question_number=question_number,
#                         question_type=question_type,
#                         question_text=question_text,
#                         answer=answer
#                     )
#                     satisfaction_response.save()
#                 except customerSatisfaction1.DoesNotExist:
#                     pass  # Handle the case where the question does not exist in the database
#         print('Survey responses submitted successfully.')
#         # Return a success response
#         return JsonResponse({'message': 'Survey responses submitted successfully.'})

#     # Handle GET requests or invalid requests
#     return JsonResponse({'error': 'Invalid request method.'}, status=400)


def submit_survey_responses(request):
    if request.method == 'POST':
        response_data = request.POST

        print("Response Data:", response_data)
        
        for key, value in response_data.items():
            question_number = key.split('_')[1]

            if key.startswith('question') and not key.endswith('_'):
                question_type = 'paragraph'
            else:
                question_type = 'multiple_choice' if key.startswith('question') else 'dropdown'

            if question_type != 'paragraph':
                try:
                    pass
                    # question_text = customerSatisfaction1.objects.get(question_number=question_number).question_text
                    # answer = value
                    # satisfaction_response = customerSatisfaction1(
                    #     question_number=question_number,
                    #     question_type=question_type,
                    #     question_text=question_text,
                    #     answer=answer
                    # )
                    # satisfaction_response.save()

                    # Print the data to the terminal
                    print("Question Number:", question_number)
                    print("Question Type:", question_type)
                    print("Question Text:", question_text)
                    print("Answer:", answer)
                    print("\n")
                    
                except ObjectDoesNotExist:
                    # Handle the case where the question does not exist in the database
                    print(f"Question {question_number} does not exist in the database.")
                except Exception as e:
                    # Handle other exceptions, if any
                    print(f"An error occurred: {str(e)}")

        print('Survey responses submitted successfully.')
        # Return a success response
        return JsonResponse({'message': 'Survey responses submitted successfully.'})

    # Handle GET requests or invalid requests
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



# from .models import *
# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import customerSatisfaction

# def submit_survey_responses(request):
#     if request.method == 'POST':
#         try:
#             question_number = request.POST.get('question_number')
#             question_type = request.POST.get('question_type')
#             question_text = request.POST.get('question_text')
#             options = request.POST.get('options')
#             answer = request.POST.get('answer')

#             # Create a new instance of the customerSatisfaction model and save it
#             satisfaction = customerSatisfaction(
#                 question_number=question_number,
#                 question_type=question_type,
#                 question_text=question_text,
#                 options=options,
#                 answer=answer
#             )
#             satisfaction.save()
#             return HttpResponse("Survey response submitted successfully!")
#         except Exception as e:
#             return HttpResponse(f"Error occurred: {str(e)}")
#     else:
#         return render(request, "Customer_satisfaction.html")


