from django.conf.urls import patterns, url

urlpatterns = patterns('infusionsoft_bmi.views',
					   url(r'^$','endpoint'),
	)