from django.conf.urls import patterns, url

urlpatterns = patterns(
    'student_profile.views',
    url(r'^$', 'index', name='profile_index'),
    url(r'^language$', 'language_change_handler', name='language_change'),
    url(r'^language/info$', 'language_info', name='released_languages'),
)
