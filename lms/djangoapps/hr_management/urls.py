from django.conf import settings
from django.conf.urls import include, patterns, url

from hr_management import views

urlpatterns = patterns(
    'hr_management.views',
    url(r'^$','index', name='index'),
    url(r'^users$','user_list', name='user_list'),
    url(r'^courses$','course_list', name='course_list'),
    url(r'^courses/{}$'.format(settings.COURSE_ID_PATTERN),'course_detail', name='course_detail'),
    url(r'^require-course-access', 'require_course_access', name='require_course_access'),
    url(r'^change-course-access', 'change_course_access', name='change_course_access'),
)
