import logging
from dateutil import parser

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from openedx.core.lib.api.authentication import (
    OAuth2AuthenticationAllowInactiveUser,
)
from openedx.core.lib.api.permissions import IsStaffOrOwner

from xmodule.modulestore.django import modulestore
from certificates.models import GeneratedCertificate

log = logging.getLogger(__name__)

class GetBatchCompletionDataView(APIView):
    authentication_classes = OAuth2AuthenticationAllowInactiveUser,
    permission_classes = IsStaffOrOwner,

    def get(self, request):
        """
            /api/course_completion/v0/batch[?time-parameter]

            time-parameter is an optional query parameter of: 
                ?updated_before=yyyy-mm-ddThh:mm:ss
                ?updated_after=yyyy-mm-ddThh:mm:ss
                ?updated_before=yyyy-mm-ddThh:mm:ss&updated_after=yyyy-mm-ddThh:mm:ss

        """
        updated_after = request.GET.get('updated_after','')
        updated_before = request.GET.get('updated_before','')

        certs = GeneratedCertificate.objects.all()
        if updated_after:
            min_date = parser.parse(updated_after)
            certs = certs.filter(created_date__gt=min_date)

        if updated_before:
            max_date = parser.parse(updated_before)
            certs = certs.filter(created_date__lt=max_date)

        cert_list = []
        for cert in certs:
            course = modulestore().get_course(cert.course_id)
            if not course:
                course_name = str(cert.course_id)
            else: 
                course_name = course.display_name

            cert_data = {
                'email': cert.user.email,
                'course_name': course_name,
                'course_id': str(cert.course_id),
                'grade': cert.grade,
                'completion_date':  str(cert.created_date)               
            }
            cert_list.append(cert_data)

        return Response(cert_list, status=200)

