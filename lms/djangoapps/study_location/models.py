# -*- coding: utf-8 -*-
"""
StudyLocations have an identifying name and a contact email
StudyLocationConfigurations allow administrators to enable
the feature and to specify a display name to override the 
default.  
"""
import datetime
import logging

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.fields.json import JSONField
from model_utils import Choices
# from model_utils.models import TimeStampedModel
# from xmodule.modulestore.django import modulestore
from config_models.models import ConfigurationModel

# LOGGER = logging.getLogger(__name__)


class StudyLocation(models.Model):
    """
    Store a name and contact email for a Study Location
    """
    class Meta(object):
        app_label = "study_location"

    location = models.CharField(max_length=100, blank=False, unique=True)
    contact_email = models.EmailField(max_length=70,blank=True, unique=True)

    # TODO: post_save, send an email to contact_email to verify?


class StudentStudyLocation(models.Model):
    """
    Associate a student with a StudyLocation.  A student can change study locations
    over time.  Since in some cases study locations may be included on a
    certificate, and we want the certificate associated with the location used
    at the time, we need to store older associations when changing to a new one.
    """

    user_id = models.ForeignKey(User)
    studylocation_id = models.ForeignKey(StudyLocation)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        # unique_together = (('user', 'course_id'),)
        app_label = "study_location"

    @classmethod
    def location_for_student(cls, student, before_when=datetime.datetime.now()):
        """
        This returns the study location for a student for a specific
        time period, or None if no such study location exits.
        Return the most recent study location prior to the date passed
        """
        try:
            return cls.objects.filter(user=student, created_date__lte=before_when).order_by('-created_date')[0]
        except cls.DoesNotExist:
            pass

        return None


class StudyLocationConfiguration(ConfigurationModel):
    """
    Configuration options for StudyLocation overall
    Currently settable is the display name 
    If there is no enabled StudyLocationConfiguration, 
    features using StudyLocation are disabled.
    """
    class Meta(ConfigurationModel.Meta):
        app_label = "study_location"

    display_name = models.CharField(
        max_length=70,
        help_text=_("Override the term used to describe study locations; e.g., training center, campus, etc. "),
        default=_("Study Location"),
    )

    @classmethod
    def display_name(cls):
        instance = cls.current()
        if instance.enabled:
            return instance.display_name
        else:
            return cls.fields['display_name'].default

    @classmethod
    def is_enabled(cls):
        instance = cls.current()
        if instance:
            return instance.enabled
        else:
            return False
