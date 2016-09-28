from django.contrib import admin

from .models import HrManager, CourseAccessRequest, CourseCCASettings, SitewideReportList

admin.site.register(HrManager)
admin.site.register(CourseAccessRequest)
admin.site.register(CourseCCASettings)
admin.site.register(SitewideReportList)