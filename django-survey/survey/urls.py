from django.conf.urls import patterns, url
from survey.views import * 

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^(?P<survey_id>\d+)/$', open_survey, name='open_survey'),
    url(r'^create_survey/$', create_survey, name='create_survey'),
    url(r'^delete_survey/(?P<survey_id>\d+)/$', delete_survey, name='delete_survey'),
    url(r'^edit_title/(?P<survey_id>\d+)/$', edit_title, name="edit_title"),
    url(r'^create_question/(?P<survey_id>\d+)/$', create_question, name='create_question'),
    url(r'^submit_survey/(?P<survey_id>\d+)/$', submit_survey, name='submit_survey'),
    url(r'^show_results/(?P<survey_id>\d+)/$', show_results, name='show_results'),
    url(r'show_image/(?P<survey_id>\d+)/(?P<question_id>\d+)/$', show_image, name='show_image'),
    url(r'^logout/$', logout, name='logout')
)