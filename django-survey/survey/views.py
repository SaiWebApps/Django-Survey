import webapp2
from google.appengine.api import users
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from survey.models import *
from survey.forms import *
from mimetypes import guess_type

################Helper Methods - Handle repeated sections of code.####################
'''Create the request context for the home page.'''
def create_default_context():
    context = {}
    # List of all surveys that have been created thus far; sorted by creation date
    context['survey_list'] = Survey.objects.all().order_by('date_created').reverse()
    # AppEngine method to get user email
    context['user_email'] = users.get_current_user().email()
    return context

'''Create the request context for a specific survey's page.'''
def create_survey_context(survey_bean):
    context = {}
    context['survey'] = survey_bean
    return context

##################Actions - mapped to specific urls in urls.py########################
'''Display home page, which consists of a list of all surveys that have been created
   thus far and a form to create new surveys. '''
def home(request):
    return render(request, 'survey/home.html', create_default_context())


'''Open the Survey with the given survey_id.'''
def open_survey(request, survey_id):
    survey_bean = get_object_or_404(Survey, pk = survey_id)
    request_context = create_survey_context(survey_bean)
   
    if survey_bean.is_survey_owner(users.get_current_user().email()):
        return render(request, 'survey/owner_detail.html', request_context)
    return render(request, 'survey/user_detail.html', request_context)

    
'''Show the results for the Survey with the given survey_id.'''
def show_results(request, survey_id):
    survey_bean = get_object_or_404(Survey, pk = survey_id)
    return render(request, 'survey/results.html', create_survey_context(survey_bean))


'''Use AppEngine-provided functionality to log the user out.'''
def logout(request):
    return redirect(users.create_logout_url('/'))


'''Create a Survey with the user-specified title.'''
def create_survey(request):
    if request.method != 'POST':
        raise Http404
   
    # Populates a SurveyForm with matching values from request.POST, which is a dict
    survey_form = SurveyForm(request.POST)
    user_email = users.get_current_user().email()  # AppEngine method to get user email
   
    if not survey_form.is_valid():  #If the new Survey's title is blank
        context = create_default_context()  #The usual context for the home page
        context['survey_form'] = survey_form  #To display form errors on the home page
        return render(request, 'survey/home.html', context)
   
    survey_bean = survey_form.save(commit = False) #Convert the form into a bean.
    survey_bean.owner_email = user_email #Set the bean's owner.
    survey_bean.save() #Save the bean in the database.
    return redirect('/survey/' + str(survey_bean.id) + '/')


'''Delete the Survey with the given survey_id.'''
def delete_survey(request, survey_id):
    if request.method != 'POST':
        raise Http404
    
    survey_bean = get_object_or_404(Survey, pk = survey_id)
    # Make sure that the deletion request came from the Survey owner. If not, display an error message.
    if not survey_bean.is_survey_owner(users.get_current_user().email()):
        context = create_default_context()
        context['privileges_error'] = 'This survey can be deleted only by its creator.'
        return render(request, 'survey/home.html', context) 
    
    survey_bean.delete() # Delete the Survey.
    return redirect('/survey/') #Redirect to prevent multiple survey creations via F5.


'''Change the title of the Survey with the given survey_id.'''
def edit_title(request, survey_id):
    survey_bean = get_object_or_404(Survey, pk = survey_id)
    
    # If we did not receive a POST request or the current user is not the
    # Survey's owner, then do not allow the user to change the Survey's title.
    if request.method != 'POST' or not survey_bean.is_survey_owner(users.get_current_user().email()):
        raise Http404
    
    survey_form = SurveyForm(request.POST)
    if survey_form.is_valid():
        survey_bean.survey_title = survey_form.cleaned_data['survey_title']
        survey_bean.save()
    
    return redirect('/survey/' + survey_id + '/')
    

'''Create a Question in the Survey with the given survey_id.'''
def create_question(request, survey_id):
    survey_bean = get_object_or_404(Survey, pk = survey_id)
    if request.method != 'POST' or not survey_bean.is_survey_owner(users.get_current_user().email()):
        raise Http404
    # request.FILES and request.POST are both dicts; QuestionForm will use these
    # arguments to set its fields to user inputs.
    # request.FILES -> for image uploads
    question_form = QuestionForm(request.POST, request.FILES)
    # Each response field had the same name - response_text - so we can access the
    # whole list of responses in the following manner.
    response_list = request.POST.getlist('response_text')
    response_form = ResponseForm()  # Will be used to validate & save Responses
   
    if not question_form.is_valid():
        context = create_survey_context(survey_bean)
        context['question_form'] = question_form  #To show form errors
        return render(request, 'survey/owner_detail.html', context)
   
    if not response_form.is_valid_response_list(response_list):  #Insufficient responses
        context = create_survey_context(survey_bean)
        context['response_error'] = 'Please specify at least 2 response options.'
        return render(request, 'survey/detail.html', context)
   
    question_bean = question_form.save(commit=False)  #Convert the form into a bean.
    question_bean.survey = survey_bean #Set the Foreign Key.
    if request.FILES:
        question_bean.image_file = request.FILES['file']
    question_bean.save()
    response_form.save_response_list(question_bean, response_list)
    
    return redirect('/survey/' + survey_id + '/')


'''Submit responses for the Survey with the given survey_id.'''
def submit_survey(request, survey_id):
    if request.method != 'POST':
        raise Http404
    
    survey_bean = get_object_or_404(Survey, pk = survey_id)

    for response_id in request.POST.values():
        response_bean = get_object_or_404(Response, pk = response_id)
        if not survey_bean.contains_response(response_bean):
            break
        response_bean.increment_votes()
        response_bean.save()

    return redirect('/survey/' + survey_id + '/')   


'''Show the image with the given question_id in the Survey 
   with the given survey_id.'''
def show_image(request, survey_id, question_id):
    question_bean = get_object_or_404(Question, pk = question_id)
    image = question_bean.image_file
    if not image:
        return redirect('/survey/' + survey_id)
    response = HttpResponse(image)
    response['Content-Type'] = guess_type(image.file.name)
    return response