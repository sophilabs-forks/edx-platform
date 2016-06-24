from django.contrib import admin

from .models import HrManager, CourseAccessRequest

admin.site.register(HrManager)
admin.site.register(CourseAccessRequest)
