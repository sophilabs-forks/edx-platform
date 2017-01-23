from django.conf.urls import url

from . import API_VERSION, views

urlpatterns = [
	url(r'^$', views.index, name='search_api_index'),
	#url(r'^{}$'.format(API_VERSION), views.index, name='search_api_index'),
	url(r'^{}/reindex_course'.format(API_VERSION),
        views.reindex_course, name='reindex_course'),
]
