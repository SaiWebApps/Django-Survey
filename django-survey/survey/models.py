from django.db import models
from datetime import datetime

class Survey(models.Model):
    survey_title = models.CharField(max_length = 200, blank = False)
    date_created = models.DateTimeField(default = datetime.today())
    owner_email = models.EmailField()
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
    def _unicode_(self):
        return self.response_text;