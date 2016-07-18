from django.contrib import admin

from .models import HrManager, CourseAccessRequest, CourseCCASettings

admin.site.register(HrManager)
admin.site.register(CourseAccessRequest)
admin.site.register(CourseCCASettings)
