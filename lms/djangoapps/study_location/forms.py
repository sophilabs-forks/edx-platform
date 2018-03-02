from django.forms import ModelForm, ModelChoiceField, ChoiceField, widgets
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings

from .models import StudyLocation, StudentStudyLocation, StudyLocationConfiguration


class StudyLocationRegistrationExtensionForm(ModelForm):

    # b/c of the way the registration extra fields code works,
    # must explicitly specify ChoiceField
    studylocationqs = StudyLocation.objects.order_by('location')
    studylocation = ModelChoiceField(queryset=studylocationqs)

    def __init__(self, *args, **kwargs):
        super(StudyLocationRegistrationExtensionForm, self).__init__(*args, **kwargs)
        display_name = StudyLocationConfiguration.get_display_name()
        self.fields['studylocation'].error_messages = {
            "required": u"Please indicate a {}.".format(display_name),
        }
        self.fields['studylocation'].help_text = (
            "Indicate the {} through which you are taking {} courses"
            ).format(display_name, settings.PLATFORM_NAME)
        self.fields['studylocation'].label = display_name

    class Meta(object):
        model = StudentStudyLocation
        fields = ('studylocation', )
        serialization_options = {
            'studylocation': {'field_type': 'select'}
        }

    @property
    def location_choices(self):
        """
        return tuple of StudyLocations with id and location name
        """
        return StudyLocation.objects.all().order_by('location')
