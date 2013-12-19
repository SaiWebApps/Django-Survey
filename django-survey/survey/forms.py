from django import forms
from django.forms import Form, ModelForm
from survey.models import *

class ProfileForm(ModelForm):
    '''Return whether a UserProfile exists for the given email'''
    def exists_profile(self, user_email):
        try:
            UserProfile.objects.get(email = user_email)
            return True
        except UserProfile.DoesNotExist:
            return False
        
    '''If there is no UserProfile for the given email, then create one.'''
    def create_profile(self, user_email):
        if self.exists_profile(user_email):
            return False
        
        user_bean = UserProfile()
        user_bean.email = user_email
        user_bean.save()
        return True
    
    class Meta:
        model = UserProfile
        fields = ['email']


class SurveyForm(ModelForm):
    survey_title = forms.CharField(max_length = 200, error_messages = {'required': 'Survey Title Required'})

    class Meta:
        model = Survey
        fields = ['survey_title']


class QuestionForm(ModelForm):
    question_text = forms.CharField(max_length = 200, error_messages = {'required' : 'Question Required'})
    image_file = forms.ImageField(required = False)
    
    class Meta:
        model = Question
        fields = ['question_text']
        

class ResponseForm(Form):
    # The user must submit at least 2 valid, complete response options
    # in order for the question and responses to be processed.
    def is_valid_response_list(self, response_list):
        num_valid_inputs = 0
        for value in response_list:
            if value.strip():
                num_valid_inputs = num_valid_inputs + 1
        if num_valid_inputs >= 2:
            return True
        return False
    
    # Save only the Response beans with non-empty response options.
    def save_response_list(self, question_bean, response_list):
        count = 0
        for value in response_list:
            if value.strip():
                response_bean = Response(response_text = value, question = question_bean)
                response_bean.position = count + 1
                count = count + 1
                response_bean.save()