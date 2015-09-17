#!/usr/bin/python
"""
django management command: create single user based on CSV string
"""
#os for devstack/testing only
import os
import csv

from django.core.management.base import BaseCommand

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from instructor.enrollment import enroll_email, get_user_email_language


class Command(BaseCommand):
    help = "Test CSV import capabilities for single user"

    def handle(self, *args, **options):

        ##### vars for testing
        user_info = os.environ['AQ_USER'].split(',')
        ##### end testing vars

        course_id_mapping = { 
            '/opt/course_export/GYM-001-Course_Progress.csv':'Gymnasium/001/0', #DEFEATING BUSY
            '/opt/course_export/GYM-002-Course_Progress.csv':'Gymnasium/002/0', #INTRODUCING NODE.JS
            '/opt/course_export/GYM-003-Course_Progress.csv':'Gymnasium/003/0', #GRID LAYOUT IN BOOTSTRAP 3
            '/opt/course_export/GYM-004-Course_Progress.csv':'Gymnasium/004/0', #CREATING A WORDPRESS THEME
            # '':'Gymnasium/005/0', #INTRODUCING SKETCH FOR UX AND UI
            '/opt/course_export/GYM-100-Course_Progress.csv':'Gymnasium/100/0', #CODING FOR DESIGNERS
            '/opt/course_export/GYM-101-Course_Progress.csv':'Gymnasium/101/0', #RESPONSIVE WEB DESIGN
            '/opt/course_export/GYM-102-Course_Progress.csv':'Gymnasium/102/0', #JQUERY BUILDING BLOCKS
            '/opt/course_export/GYM-103-Course_Progress.csv':'Gymnasium/103/0', #UX FUNDAMENTALS
            '/opt/course_export/GYM-104-Course_Progress.csv':'Gymnasium/104/0', #JAVASCRIPT FOUNDATIONS
            # '':'Gymnasium/105/0', #WRITING FOR WEB & MOBILE
            # '':'Gymnasium/106/0', #INFORMATION DESIGN AND VISUALIZATION FUNDAMENTALS
            }

        ###probably not needed for this part
        # user_csv = '/opt/course_export/Student_Activity.csv'
        # with open(user_csv,'rU') as f:
        #     reader = csv.reader(f)
        #     user_list = list(reader)

        #grabbing stats
        user_actions = {}
        total_enrollments = 0
        unique_user_enrollments = 0
        for csv_file, course_id in course_id_mapping.iteritems():
            #  print csv_file + " - " + course_id
            email = user_info[2]

            with open(csv_file,'rU') as f:
                reader = csv.reader(f)
                data = list(reader)

                #strip off first line column names
                data = data[1:]
                for d in data:
                    course_email = d[0]

                    if not course_email in user_actions.keys():
                        user_actions[course_email] = []
                        unique_user_enrollments += 1

                    user_actions[course_email].append(course_id)
                    total_enrollments += 1

            print 'done with: %s' % csv_file

        #write actions to sample csv file
        with open('/tmp/course_enrollment_output.txt','wb') as f:
            for user, actions in iter(sorted(user_actions.iteritems())):
                f.write('%s: %s\n' % (user, ', '.join(actions)))

        print 'total enrollments: %d' % total_enrollments
        print 'unique users enrolled: %d' % unique_user_enrollments

            # # #workflow from lms/djangoapps/instructor/views/api.py:students_update_enrollmen
            # # #def students_update_enrollment(request, course_id):
            # course_id = SlashSeparatedCourseKey.from_deprecated_string(course_id)
            # action = 'enroll'
            # # identifiers_raw = request.POST.get('identifiers')
            # # identifiers = _split_input_list(identifiers_raw)
            # auto_enroll = True
            # email_students = False


        # email = user_info[2] #skipping email validation
        # email_params = {}
        # language = get_user_email_language(None)

        # before, after = enroll_email(course_id, email, auto_enroll, email_students, email_params, language=language)
        
        # print '---- user enrolled ----'
        # print before
        # print after

