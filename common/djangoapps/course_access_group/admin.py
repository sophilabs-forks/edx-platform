"""
Admin site bindings for course_access_group
"""

from django.contrib import admin

# from config_models.admin import ConfigurationModelAdmin
from .models import CourseAccessGroup, DomainBlacklist

admin.site.register(CourseAccessGroup)
admin.site.register(DomainBlacklist)
