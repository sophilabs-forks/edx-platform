from django.core.urlresolvers import reverse

from student_account.fields import AccountSettingsExtensionField


class StudyLocationExtensionField(AccountSettingsExtensionField):

    field_id = 'study_location'
    js_model = 'js/study_location/models/student_study_location'
    js_field_view_class = 'FieldViews.DropdownFieldView'
    api_url = None
    title = 'Study Location'
    helpMessage = 'What should go here?'
    valueAttribute = 'study_location'
    options= [(1, 'One'), (2, 'Two'), ]
    persistChanges = True 

    def __init__(self, request):
        self.api_url = reverse("accounts_api", kwargs={'username': request.user.username})
        self.title = "this will be an override based on the study location config model"

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
