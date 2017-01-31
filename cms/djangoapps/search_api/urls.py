from django.conf.urls import url

from . import API_VERSION, views

urlpatterns = [
    url(r'^$', views.index, name='search_api_index'),
    url(r'^{}/reindex_course'.format(API_VERSION),
        views.CourseIndexer.as_view(), name='reindex-course'),
]
