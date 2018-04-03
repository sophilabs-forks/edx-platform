"""
Tests for the Appsembler API views.
"""

from urllib import quote, urlencode

from django.core.urlresolvers import reverse

from lms.djangoapps.course_api.tests.test_views import CourseApiTestViewMixin
import json
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

from django.test.utils import override_settings

from search.tests.test_course_discovery import DemoCourse


### for this endpoint test
from mock import patch
from datetime import datetime
from rest_framework.permissions import AllowAny
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
# from openedx.core.lib.api.authentication import OAuth2AuthenticationAllowInactiveUser


from student.tests.factories import UserFactory, CourseEnrollmentFactory
from xmodule.modulestore.tests.factories import CourseFactory
from certificates.models import GeneratedCertificate

from appsembler_api.views import GetBatchEnrollmentDataView

# @patch('appsembler_api.views.GetBatchEnrollmentDataView.permission_classes', [AllowAny])
# @patch('appsembler_api.views.GetBatchEnrollmentDataView.authentication_classes', [])
@patch('appsembler_api.views.GetBatchEnrollmentDataView.authentication_classes', [])
@patch('appsembler_api.views.GetBatchEnrollmentDataView.permission_classes', [AllowAny])
class AnalyticsEnrollmentBatchViewTest(CourseApiTestViewMixin, ModuleStoreTestCase):
    """
    Tests for the endpoint: /analytics/enrollment/batch
    """

    USERNAME = "Bob"
    EMAIL = "bob@example.com"
    PASSWORD = "edx"

    def setUp(self):
        super(AnalyticsEnrollmentBatchViewTest, self).setUp()
        
        self.view = GetBatchEnrollmentDataView.as_view()

        self.staff = UserFactory.create(
            username=self.USERNAME,
            email=self.EMAIL,
            password=self.PASSWORD,
            is_staff=True,
        )
        self.request_factory = APIRequestFactory()

        self.course1 = CourseFactory()
        self.course2 = CourseFactory()

        test_time = datetime(year=1999, month=1, day=1, minute=0, second=0)

        #enrollment dates at years 2000, 2010, 2020
        self.enrollments = [
            CourseEnrollmentFactory(course_id=self.course1.id, created=test_time.replace(year=2000)),
            CourseEnrollmentFactory(course_id=self.course1.id, created=test_time.replace(year=2010)),
            CourseEnrollmentFactory(course_id=self.course1.id, created=test_time.replace(year=2020)),
            CourseEnrollmentFactory(course_id=self.course2.id, created=test_time.replace(year=2020)),
        ]

        #certificate issue dates at years 2005, 2015, 2025
        self.certificates = [ GeneratedCertificate(
                                course_id=ce.course_id, 
                                user=ce.user, 
                                created_date=ce.created.replace(year=ce.created.year+5)
                            ) 
                                for ce in self.enrollments
                        ]

        self.url = reverse('get_batch_user_data')

    def test_analytics_enrollment_endpoint_alone(self):
        request = self.request_factory.get(self.url, content_type='application/json')
        force_authenticate(request, user=self.staff)
        res = self.view(request)
        res.render()

        # res = self.client.get(self.url)
        print res.content
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.status_code,4)
        # self.assertEqual(len(self.certificates),4)

