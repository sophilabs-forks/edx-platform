from django.conf.urls import patterns, url

urlpatterns = patterns(
    'student_profile.views',
    url(r'^$', 'index', name='profile_index'),
    url(r'^preferences$', 'update_preferences', name='change_preferences'),
    url(r'^preferences/languages$', 'language_info', name='language_info'),
)
