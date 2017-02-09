from django.conf.urls import patterns, url 

from .views import GetBatchCompletionDataView

urlpatterns = patterns(
    '', 
    url(r'^v0/batch', GetBatchCompletionDataView.as_view(), name="get_batch_completion_data"),
)
