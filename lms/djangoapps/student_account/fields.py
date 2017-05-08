from abc import ABCMeta, abstractproperty

from django.conf.urls import reverse


class AccountSettingsExtensionField(object):
    """
    Abstract Base Class for Account Settings extension fields.
    Extension field classes must subclass this class.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def field_id(self):
        """
        set the field id
        """
        raise NotImplementedError

    @abstractproperty
    def js_model(self):
        """
        set the Backbone model associated with the Django model 
        for this field
        """
        raise NotImplementedError

    @abstractproperty
    def js_field_class(self):
        """
        set the field class for use in the Backbone application
        """
        raise NotImplementedError       

    @abstractproperty
    def api_url(self):
        """
        set the API url used to get/set values to/from the Django model 
        for this field
        """     
        raise NotImplementedError


# the below wouldn't be defined here, but in some other module
# or add on app
class BryanTestExtensionField(AccountSettingsExtensionField):

    field_id = 'bryan_test'
    js_model = 'js/student_account/models/user_account_model'
    js_field_class = 'AccountSettingsFieldViews.DropdownFieldView'
    api_url = None

    def __init__(self, request):
        self.api_url = reverse("accounts_api", kwargs={'username': request.user.username})

        return {
            'id': self.field_id,
            'js_model': self.js_model,
            'js_field_class': self.js_field_class,
            'api_url': self.api_url,
            'title': 'Bryan Test field',
            'helpMessage': 'Hey, does this help?',
            'valueAttribute': 'bryan_test',
            'options': [(1, 'One'), (2, 'Two'), ],
            'persistChanges': True
        }
