from smtplib import SMTPException

from celery.task import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from student.models import CourseEnrollment
from xmodule.modulestore.django import modulestore
from organizations.models import Organization

from .utils import generate_csv_grade_string
from .models import HrManager, SitewideReportList

LOGGER = get_task_logger(__name__)


@task()
def send_email_to_user(subject, message, from_address, email_addresses):
    """ Updates course search index. """
    for email in email_addresses:
        try:
            send_mail(subject, message, from_address, [email])
        except SMTPException as exc:
            LOGGER.error('Error sending email to {}'.format(email))
        else:
            LOGGER.debug('Successfully sent email to {}'.format(email))

@task()
def generate_and_email_nyif_report():
    """ 
    This should happen on the first of every month. 
    Generates a sitewide report
    """

    total_users = len(User.objects.all())
    total_courses = len(modulestore().get_courses())
    total_enrollments = len(CourseEnrollment.objects.all())
    total_organizations = len(Organization.objects.all())

    raw_grade_data = generate_csv_grade_string()
    last_month = (date.today().replace(day=1) - timedelta(days=1)).strftime('%B')

    email_subject = 'NYIF CCA Report for {}'.format(last_month)
    email_content = """
NYIF Corporate Client Report
{date}

Overview
    Number of Users: {num_users}
    Number of Courses: {num_courses}
    Number of Enrollments: {num_enrollments}
    Number of Organizations {num_organizations}

Raw student grade data
{grade_data}
    """.format(date=datetime.now().date(),
            num_users=total_users,
            num_courses=total_courses,
            num_enrollments=total_enrollments,
            num_organizations=total_organizations,
            grade_data=raw_grade_data
        )
    for report_recipient in SitewideReportList.objects.all():
        if report_recipient.send_monthly_report:
            send_mail(email_subject, email_content, settings.DEFAULT_FROM_EMAIL, ['tj@appsembler.com'])
            # send_mail(email_subject, email_content, settings.DEFAULT_FROM_EMAIL, [report_recipient.email])

#TODO: refactor into above method
@task()
def generate_and_email_customer_report():
    """ 
    This should happen on the first of every month. 
    Generates a customer report based on microsite organization
    """

    for organization in Organization.objects.all():
        total_users = len(organization.users.all())

        total_enrollments = 0
        courses = [ c for c in mongo_courses if c.org==org_string ]
        total_courses = len(courses)
        for course in courses:
            enrollments = CourseEnrollment.objects.filter(course_id=course.id)
            total_enrollments += len(enrollments)


        raw_grade_data = generate_csv_grade_string(organization=organization)
        last_month = (date.today().replace(day=1) - timedelta(days=1)).strftime('%B')

        email_subject = '{} Report for {}'.format(organization.name,last_month)
        email_content = """
{org_name} Report
{date}

Overview
    Number of Users: {num_users}
    Number of Courses: {num_courses}
    Number of Enrollments: {num_enrollments}

Raw student grade data
{grade_data}
        """.format(org_name=organization.name,
                date=datetime.now().date(),
                num_users=total_users,
                num_courses=total_courses,
                num_enrollments=total_enrollments,
                grade_data=raw_grade_data
            )
        #send to all users who are marked to receive the email
        for manager in HrManager.objects.filter(organization=organization):
            if manager.send_monthly_report:
                send_mail(email_subject, email_content, settings.DEFAULT_FROM_EMAIL, ['tj@appsembler.com'])
                # send_mail(email_subject, email_content, settings.DEFAULT_FROM_EMAIL, [manager.user.email])
