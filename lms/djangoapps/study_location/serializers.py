from rest_framework import serializers
from openedx.core.djangoapps.user_api.serializers import ReadOnlyFieldsSerializerMixin

from .models import StudentStudyLocation


class StudentStudyLocationSerializer(serializers.ModelSerializer, ReadOnlyFieldsSerializerMixin):
    """
    Class that serializes the portion of User model needed for account information.
    """
    class Meta:
        model = StudentStudyLocation
        fields = ("user", "studylocation", )
        # read_only_fields = ()
        # explicit_read_only_fields = ("created_date")
