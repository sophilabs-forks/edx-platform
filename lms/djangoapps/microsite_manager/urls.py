from django.conf import settings
from django.conf.urls import include, patterns, url

from microsite_manager import views

urlpatterns = patterns(
    'microsite_manager.views',
    url(r'^$','index', name='index'),
    url(r'^add-microsite', 'add_microsite', name='add_microsite'),
)
