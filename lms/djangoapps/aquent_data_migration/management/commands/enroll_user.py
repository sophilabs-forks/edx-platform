#!/usr/bin/python
"""
django management command: create single user based on CSV string
"""
#os for devstack/testing only
import os

from django.core.management.base import BaseCommand

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from instructor.enrollment import enroll_email, get_user_email_language


class Command(BaseCommand):
    help = "Test CSV import capabilities for single user"

    def handle(self, *args, **options):

        ##### vars for testing
        user_info = os.environ['AQ_USER'].split(',')
        course_info = os.environ['AQ_COURSE'].split(',')
        course_id = 'Gymnasium/100/0'
        ##### end testing vars

        #for user in users
        #for course in courses
        
        #workflow from lms/djangoapps/instructor/views/api.py:students_update_enrollmen
        #def students_update_enrollment(request, course_id):
        course_id = SlashSeparatedCourseKey.from_deprecated_string(course_id)
        action = 'enroll'
        # identifiers_raw = request.POST.get('identifiers')
        # identifiers = _split_input_list(identifiers_raw)
        auto_enroll = True
        email_students = False


        email = user_info[2] #skipping email validation
        email_params = {}
        language = get_user_email_language(None)

        before, after = enroll_email(course_id, email, auto_enroll, email_students, email_params, language=language)
        
        print '---- user enrolled ----'
        print before
        print after

