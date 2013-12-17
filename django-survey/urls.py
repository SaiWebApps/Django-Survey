from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/survey/', }),
    url(r'^survey/', include('survey.urls', namespace="survey")),
)