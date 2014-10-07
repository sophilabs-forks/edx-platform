"""
Single page performance tests for LMS.
"""
from bok_choy.web_app_test import WebAppTest, with_cache
from ..pages.lms.auto_auth import AutoAuthPage
from ..pages.lms.courseware import CoursewarePage
from ..pages.lms.dashboard import DashboardPage
from ..pages.lms.course_info import CourseInfoPage
from ..pages.lms.login import LoginPage
from ..pages.lms.progress import ProgressPage
from ..pages.common.logout import LogoutPage
from ..fixtures.course import CourseFixture, XBlockFixtureDesc, CourseUpdateDesc
from ..tests.helpers import UniqueCourseTest, load_data_str
from nose.plugins.attrib import attr


@attr(har_mode='explicit')
class LMSPagePerformanceTest(UniqueCourseTest):
    """
    Base class to capture LMS performance with HTTP Archives.
    """
    username = 'test_student'
    email = 'student101@example.com'

    def setUp(self):
        """
        Setup course
        """
        super(LMSPagePerformanceTest, self).setUp()

        # Install a course with sections/problems, tabs, updates, and handouts
        course_fix = CourseFixture(
            self.course_info['org'], self.course_info['number'],
            self.course_info['run'], self.course_info['display_name']
        )

        course_fix.add_update(CourseUpdateDesc(date='January 29, 2014', content='Test course update1'))
        course_fix.add_update(CourseUpdateDesc(date='January 30, 2014', content='Test course update2'))
        course_fix.add_update(CourseUpdateDesc(date='January 31, 2014', content='Test course update3'))

        course_fix.add_children(
            XBlockFixtureDesc('chapter', 'Test Section 1').add_children(
                XBlockFixtureDesc('sequential', 'Test Subsection 1').add_children(
                    XBlockFixtureDesc('problem', 'Test Problem 1', data=load_data_str('multiple_choice.xml')),
                    XBlockFixtureDesc('problem', 'Test Problem 2', data=load_data_str('formula_problem.xml')),
                    XBlockFixtureDesc('html', 'Test HTML', data="<html>Html child text</html>"),
                )
            ),
            XBlockFixtureDesc('chapter', 'Test Section 2').add_children(
                XBlockFixtureDesc('sequential', 'Test Subsection 2').add_children(
                    XBlockFixtureDesc('html', 'Html Child', data="<html>Html child text</html>")
                )
            ),
            XBlockFixtureDesc('chapter', 'Test Section 3').add_children(
                XBlockFixtureDesc('sequential', 'Test Subsection 3').add_children(
                    XBlockFixtureDesc('problem', 'Test Problem 3')
                )
            )
        ).install()

        AutoAuthPage(self.browser, username=self.username, email=self.email, course_id=self.course_id).visit()

    def record_visit_coursware(self):
        """
        Produce a HAR for loading the Coursware page.
        """
        courseware_page = CoursewarePage(self.browser, self.course_id)
        har_name = 'CoursewarePage_{}'.format(self.course_id.replace('/', '_'))

        self.courseware_page = CoursewarePage(self.browser, self.course_id)

        self.har_capturer.add_page(self.browser, har_name)
        courseware_page.visit()
        self.har_capturer.save_har(self.browser, har_name)

    def record_visit_dashboard(self):
        """
        Produce a HAR for loading the Dashboard page.
        """
        dashboard_page = DashboardPage(self.browser)
        har_name = 'DashboardPage_{}'.format(self.course_id.replace('/', '_'))

        self.har_capturer.add_page(self.browser, har_name)
        dashboard_page.visit()
        self.har_capturer.save_har(self.browser, har_name)

    def record_visit_course_info(self):
        """
        Produce a HAR for loading the Course Info page.
        """
        course_info_page = CourseInfoPage(self.browser, self.course_id)
        har_name = 'CourseInfoPage_{}'.format(self.course_id.replace('/', '_'))

        self.har_capturer.add_page(self.browser, har_name)
        course_info_page.visit()
        self.har_capturer.save_har(self.browser, har_name)

    def record_visit_login_page(self):
        """
        Produce a HAR for loading the Login page.
        """
        login_page = LoginPage(self.browser)
        har_name = 'LoginPage_{}'.format(self.course_id.replace('/', '_'))

        self.har_capturer.add_page(self.browser, har_name)
        login_page.visit()
        self.har_capturer.save_har(self.browser, har_name)

    def record_visit_progress_page(self):
        """
        Produce a HAR for loading the Progress page.
        """
        progress_page = ProgressPage(self.browser, self.course_id)
        har_name = 'ProgressPage_{}'.format(self.course_id.replace('/', '_'))

        self.har_capturer.add_page(self.browser, har_name)
        progress_page.visit()
        self.har_capturer.save_har(self.browser, har_name)


class LmsPerformanceTest(LMSPagePerformanceTest):
    """
    Test LMS performance.
    """

    @with_cache
    def test_visit_coursware(self):
        """
        Record visiting Coursware page.
        """
        self.record_visit_coursware()

    @with_cache
    def test_visit_dashboard(self):
        """
        Record visiting Dashboard page.
        """
        self.record_visit_dashboard()

    @with_cache
    def test_visit_course_info(self):
        """
        Record visiting Course Info page.
        """
        self.record_visit_course_info()

    @with_cache
    def test_visit_login_page(self):
        """
        Record visiting Login page.
        """
        LogoutPage(self.browser).visit()
        self.record_visit_login_page()

    @with_cache
    def test_visit_progress_page(self):
        """
        Record visiting Progress page.
        """
        self.record_visit_progress_page()
