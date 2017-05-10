import logging

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from student_account.fields import AccountSettingsExtensionField

from .models import StudyLocationConfiguration, StudyLocation

logger = logging.getLogger(__name__)


class StudyLocationExtensionField(AccountSettingsExtensionField):

    field_id = 'studylocation_id'
    js_model = 'js/study_location/models/student_study_location'
    js_field_view_class = 'FieldViews.DropdownFieldView'
    api_url = None
    title = 'Study Location'
    helpMessage = ''
    valueAttribute = 'studylocation_id'
    options= []
    persistChanges = True 

    def __init__(self, request):
        if not StudyLocationConfiguration.is_enabled:
            msg = _( ("To use a StudyLocationExtensionField for Account Settings, "
                      "you must enable a StudyLocationConfiguration through the "
                      "Django admin panel. Ignoring extension field.")
                   )
            logger.warn(msg)
            raise ImproperlyConfigured(msg)

        config_display_name = StudyLocationConfiguration.get_display_name()
        self.api_url = reverse("student_studylocation_api", kwargs={'username': request.user.username})
        self.title = config_display_name
        self.helpMessage = "The {} through which you take your courses".format(config_display_name.lower())
        self.options = [(sloc.id, sloc.location) for sloc in StudyLocation.objects.all().order_by('location')]

    def __call__(self):
        return {
            'id': self.field_id,
            'js_model': self.js_model,
            'js_field_view_class': self.js_field_view_class,
            'api_url': self.api_url,
            'title': self.title,
            'helpMessage': self.helpMessage,
            'valueAttribute': self.valueAttribute,
            'options': self.options,
            'persistChanges': self.persistChanges
        }
