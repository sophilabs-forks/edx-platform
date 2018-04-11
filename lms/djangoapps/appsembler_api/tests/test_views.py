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

import ddt

### for this endpoint test
from mock import patch
from datetime import datetime
import pytz
from rest_framework.permissions import AllowAny
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
# from openedx.core.lib.api.authentication import OAuth2AuthenticationAllowInactiveUser


from student.tests.factories import UserFactory, CourseEnrollmentFactory
from xmodule.modulestore.tests.factories import CourseFactory
from certificates.models import GeneratedCertificate

# from appsembler_api.views import GetBatchEnrollmentDataView

# @patch.object(GetBatchEnrollmentDataView, 'permission_classes', [AllowAny])
# @patch('appsembler_api.views.GetBatchEnrollmentDataView.authentication_classes', [])
@ddt.ddt
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
        
        # self.view = GetBatchEnrollmentDataView.as_view()

        self.staff = UserFactory.create(
            username=self.USERNAME,
            email=self.EMAIL,
            password=self.PASSWORD,
            is_staff=True,
        )
        self.request_factory = APIRequestFactory()

        self.course1 = CourseFactory()
        self.course2 = CourseFactory()

        test_time = datetime(year=1999, month=1, day=1, minute=0, second=0, tzinfo=pytz.UTC)

        #enrollment dates at years 2000, 2010, 2020
        self.enrollments = [
            CourseEnrollmentFactory(course_id=self.course1.id),
            CourseEnrollmentFactory(course_id=self.course1.id),
            CourseEnrollmentFactory(course_id=self.course1.id),
            CourseEnrollmentFactory(course_id=self.course2.id),
        ]

        # enrollment dates need to be updated after CourseEnrollments are saved to db
        updated_enrollment_years = [2000, 2010, 2020, 2020]
        for index, enrollment in enumerate(self.enrollments):
            enrollment.created = test_time.replace(year=updated_enrollment_years[index])
            enrollment.save()

        for ce in self.enrollments: 
            GeneratedCertificate(
                            course_id=ce.course_id, 
                            user=ce.user, 
                            # created_date=ce.created.replace(year=ce.created.year+5)
                        ).save()
                                
        self.certificates = list(GeneratedCertificate.objects.all())
        # certificate issue dates at years 2005, 2015, 2025 (five years after each enrollment)
        #   likewise, these values need to be updated after GeneratedCertificates are saved to db
        print len(self.enrollments), len(self.certificates)
        print type(self.enrollments), type(self.enrollments[0])
        print type(self.certificates), type(self.certificates[0])
        for enrollment, certificate in zip(self.enrollments, self.certificates):
            #get matching CourseEnrollment object
            certificate.created_date = enrollment.created.replace(enrollment.created.year + 5)
            certificate.save()

        self.url = reverse('get_batch_enrollment_data')

    @ddt.unpack
    @ddt.data(  {'course_str': 'course1', 'num_enrollments': 3},
                {'course_str': 'course2', 'num_enrollments': 1},)
    def test_analytics_enrollment_endpoint_with_only_course_id(self, course_str, num_enrollments):

        course = getattr(self, course_str)
        course_id = str(course.id)

        res = self.client.get(self.url + '?course_id={}'.format(course_id))

        self.assertIn('enrollment', res.content)
        self.assertEqual(res.status_code, 200)

        data = res.data
        self.assertEqual(len(data), num_enrollments)

    @ddt.unpack
    @ddt.data(  {'course_str': 'course1', 'query_string': 'updated_min=2030-01-01T00:00:00', 'num_enrollments': 0}, # outside range
                {'course_str': 'course1', 'query_string': 'updated_min=2001-01-01T00:00:00', 'num_enrollments': 3}, # one cert, two enrollments
                {'course_str': 'course1', 'query_string': 'updated_max=2011-01-01T00:00:00', 'num_enrollments': 2}, # two enrollments
                {'course_str': 'course1', 'query_string': 'updated_min=2001-01-01T00:00:00&updated_max=2021-01-01T00:00:00', 'num_enrollments': 3},) # one cert, two enrollments
    def test_analytics_enrollment_endpoint_with_query_strings(self, course_str, query_string, num_enrollments):

        course = getattr(self, course_str)
        course_id = str(course.id)

        res = self.client.get(self.url + '?course_id={}&{}'.format(course_id, query_string))

        if num_enrollments > 0:
            print 'qs: ' + query_string
            print res.content
            self.assertIn('enrollment', res.content)
        self.assertEqual(res.status_code, 200)

        data = res.data
        self.assertEqual(len(data), num_enrollments)
