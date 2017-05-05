"""
django admin pages for student_location models
"""
from django.contrib import admin
from config_models.admin import ConfigurationModelAdmin
from study_location.models import (
    StudyLocation,
    StudyLocationConfiguration,
)

admin.site.register(StudyLocation)
admin.site.register(StudyLocationConfiguration, ConfigurationModelAdmin)
