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

from student.tests.factories import UserFactory, CourseEnrollmentFactory
from xmodule.modulestore.tests.factories import CourseFactory
from certificates.models import GeneratedCertificate

from appsembler_api.views import GetBatchEnrollmentDataView

# @override_settings(SEARCH_ENGINE="search.tests.mock_search_engine.MockSearchEngine")
@patch.object(GetBatchEnrollmentDataView, 'permission_classes', [AllowAny])
class AnalyticsEnrollmentBatchViewTest(CourseApiTestViewMixin, ModuleStoreTestCase):
    """
    Tests for the endpoint: /analytics/enrollment/batch
    """

    # def setUp(self):
    #     super(AnalyticsEnrollmentBatchViewTest, self).setUp()
    #     DemoCourse.reset_count()
    #     self.searcher.destroy()

    #     self.courses = [
    #         self.add_course("OrgA", "Find this one with the right parameter"),
    #         self.add_course("OrgB", "Find this one with another parameter"),
    #         self.add_course("OrgC", "Find this one somehow"),
    #     ]

    #     self.url = reverse('course-list')
    #     self.staff_user = self.create_user(username='staff', is_staff=True)
    #     self.honor_user = self.create_user(username='honor', is_staff=False)

    # def add_course(self, org_code, short_description):
    #     """
    #     Add a course to both database and search.
    #     Warning: A ton of gluing here! If this fails, double check both CourseListViewTestCase and MockSearchUrlTest.
    #     """

    #     search_course = DemoCourse.get({
    #         "org": org_code,
    #         "run": "2010",
    #         "number": "DemoZ",
    #         "id": "{org_code}/DemoZ/2010".format(org_code=org_code),
    #         "content": {
    #             "short_description": short_description,
    #         },
    #     })

    #     DemoCourse.index(self.searcher, [search_course])

    #     org, course, run = search_course['id'].split('/')

    #     db_course = self.create_course(
    #         org=org,
    #         course=course,
    #         run=run,
    #         short_description=short_description,
    #     )

    #     return db_course

    # def search_request(self, search_term=''):
    #     res = self.client.get(reverse("course_list_search"), data={'search_term': search_term})
    #     return res.status_code, json.loads(res.content)

    # def test_search_api_alone(self):
    #     """
    #     Double check that search alone works fine.
    #     """
    #     res = self.client.post(reverse('course_discovery'))
    #     data = json.loads(res.content)
    #     self.assertNotEqual(data["results"], [])
    #     self.assertNotIn('course-v1', unicode(self.courses[0].id))
    #     self.assertContains(res, unicode(self.courses[0].id))
    #     self.assertEqual(data["total"], 3)

    # def test_course_api_alone(self):
    #     """
    #     Double check that search alone works fine.
    #     """
    #     self.setup_user(self.staff_user)
    #     response = self.verify_response(expected_status_code=200, params={'username': self.staff_user.username})
    #     data = json.loads(response.content)
    #     self.assertNotEqual(data["results"], [])
    #     self.assertEqual(data["pagination"]["count"], 3)
    #     self.assertNotIn('course-v1', response.content)

    # def test_list_all(self):
    #     """ test searching using the url """
    #     code, data = self.search_request()
    #     self.assertEqual(200, code)
    #     self.assertIn("results", data)
    #     self.assertNotEqual(data["results"], [])
    #     self.assertEqual(data["pagination"]["count"], 3)

    # def test_list_all_with_search_term(self):
    #     """ test searching using the url """
    #     code, data = self.search_request(search_term='somehow')
    #     self.assertEqual(200, code)
    #     self.assertIn("results", data)
    #     self.assertNotEqual(data["results"], [])
    #     self.assertEqual(data["pagination"]["count"], 1)

@patch.object(GetBatchEnrollmentDataView, 'permission_classes', [AllowAny])
class AnalyticsEnrollmentBatchViewTest(CourseApiTestViewMixin, ModuleStoreTestCase):
    """
    Tests for the endpoint: /analytics/enrollment/batch
    """

    def setUp(self):
        super(AnalyticsEnrollmentBatchViewTest, self).setUp()
        
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
        res = self.client.get(self.url)
        print res
        self.assertEqual(res.status_code,4)
        self.assertEquel(GeneratedCertificate.objects.count(),4)