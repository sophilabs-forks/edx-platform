from django.forms import ModelForm, ChoiceField
from django.db.models.fields import BLANK_CHOICE_DASH

from .models import StudyLocation, StudyLocationConfiguration


class StudyLocationRegistrationExtensionForm(ModelForm):

    # b/c of the way the registration extra fields code works,
    # must explicitly specify ChoiceField
    location = ChoiceField(label="Study Location", choices=BLANK_CHOICE_DASH + [])

    def __init__(self, *args, **kwargs):
        super(StudyLocationRegistrationExtensionForm, self).__init__(*args, **kwargs)
        self.fields['location'].error_messages = {
            "required": u"Please indicate a {}.".format(StudyLocationConfiguration.display_name),
        }
        self.fields['location'].label = StudyLocationConfiguration.display_name
        self.fields['location'].choices = BLANK_CHOICE_DASH + self.location_choices

    class Meta(object):
        model = StudentStudyLocation
        fields = ('studylocation', )

    # @property
    # def location_display_name(self):
    #     """
    #     return string of configured display name from active StudyLocationConfiguration,
    #     if there is one; otherwise, the default
    #     """
    #     return self.display_name

    @property
    def location_choices(self):
        """
        return tuple of StudyLocations with id and location name
        """
        return StudyLocation.objects.all().order_by('location')

