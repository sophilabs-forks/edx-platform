"""
URLs for the study_location app.
"""

from django.conf.urls import patterns, url
from django.conf import settings

from study_location.views import api


USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'

urlpatterns = patterns(
    '',
    url(
        r'^api/v1/studylocation/{}$'.format(USERNAME_PATTERN),
        api.StudentStudyLocationView.as_view(),
        name="student_studylocation_api"
    ),
)