"""
django admin pages for student_location models
"""
from django.contrib import admin
from config_models.admin import ConfigurationModelAdmin
from study_location.models import (
    StudyLocation,
    StudyLocationConfiguration,
)


class StudyLocationAdmin(admin.ModelAdmin):
    """
    Django admin customizations for StudyLocation model
    """
    list_display = ('location', 'contact_email',)


admin.site.register(StudyLocation, StudyLocationAdmin)
admin.site.register(StudyLocationConfiguration, ConfigurationModelAdmin)
