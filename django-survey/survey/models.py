from django.db import models
from datetime import datetime

class UserProfile(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    employer = models.CharField(max_length = 200)
    photo = models.ImageField(upload_to = None, blank = True, null = True)

    def _unicode(self):
        return self.email

class Survey(models.Model):
    survey_title = models.CharField(max_length = 200, blank = False)
    date_created = models.DateTimeField(default = datetime.today())
    owner = models.ForeignKey(UserProfile)
    
    '''Determines if the current user is the Survey owner'''
    def is_survey_owner(self, current_user):
        return current_user == self.owner.email

    '''Delete this Survey, along with all Q&A associated w/ it.'''
    def delete(self):
        for question_bean in self.question_set.all():
            for response_bean in question_bean.response_set.all():
                response_bean.delete()
            question_bean.delete()
        super(Survey, self).delete()

    def contains_response(self, response_bean):
        for question_bean in self.question_set.all():
            if response_bean in question_bean.response_set.all():
                return True
        return False

    def _unicode_(self):
        return self.survey_title


class Question(models.Model):
    survey = models.ForeignKey(Survey)
    question_text = models.CharField(max_length = 200, blank = False)
    image_file = models.ImageField(upload_to = None, blank = True, null = True)

    def _unicode_(self):
        return self.question_text
        
    class Meta:
        order_with_respect_to = "survey"

        
class Response(models.Model):
    question = models.ForeignKey(Question)
    response_text = models.CharField(max_length = 200, blank = False)
    votes = models.IntegerField(default=0)
    position = models.IntegerField(default = 0)
    
    '''Increment the number of times that this response was chosen.'''
    def increment_votes(self):
        self.votes = self.votes + 1
        
    def _unicode_(self):
        return self.response_text;