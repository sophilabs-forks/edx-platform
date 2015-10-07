#!/usr/bin/python
"""
django management command: create single user based on CSV string
"""
#os for devstack/testing only
import os
import csv
import json
import urllib

from django.core.management.base import BaseCommand

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from instructor.enrollment import enroll_email, get_user_email_language


class Command(BaseCommand):
    help = "Test CSV import capabilities for single user"

    def handle(self, *args, **options):

        ##### vars for testing
        #user_info = os.environ['AQ_USER'].split(',')
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

        course_name_mapping = { #could have pulled from db, but this is easier
            'Gymnasium/001/0': "Defeating Busy", #DEFEATING BUSY
            'Gymnasium/002/0': "Intruducing Node.js", #INTRODUCING NODE.JS
            'Gymnasium/003/0': "Grid Layout in Bootstrap 3", #GRID LAYOUT IN BOOTSTRAP 3
            'Gymnasium/004/0': "Creating a Wordpress Theme",  #CREATING A WORDPRESS THEME
            'Gymnasium/100/0': "Coding for Designers", #CODING FOR DESIGNERS
            'Gymnasium/101/0': "Responsive Web Design", #RESPONSIVE WEB DESIGN
            'Gymnasium/102/0': "JQuery Building Blocks", #JQUERY BUILDING BLOCKS
            'Gymnasium/103/0': "UX Fundamentals", #UX FUNDAMENTALS
            'Gymnasium/104/0': "Javascript Foundations" #JAVASCRIPT FOUNDATIONS
            }

        #### getting messy with all of these mappings
        course_prefix_mapping = { 
            'Gymnasium/001/0': "DB", #DEFEATING BUSY
            'Gymnasium/002/0': "NJS", #INTRODUCING NODE.JS
            'Gymnasium/003/0': "GLB", #GRID LAYOUT IN BOOTSTRAP 3
            'Gymnasium/004/0': "CWT",  #CREATING A WORDPRESS THEME
            'Gymnasium/100/0': "CFD", #CODING FOR DESIGNERS
            'Gymnasium/101/0': "RWD", #RESPONSIVE WEB DESIGN
            'Gymnasium/102/0': "JBB", #JQUERY BUILDING BLOCKS
            'Gymnasium/103/0': "UXF", #UX FUNDAMENTALS
            'Gymnasium/104/0': "JSF" #JAVASCRIPT FOUNDATIONS
            }

        course_index_mapping = { 
            'Gymnasium/001/0': 0, #DEFEATING BUSY
            'Gymnasium/002/0': 1, #INTRODUCING NODE.JS
            'Gymnasium/003/0': 2, #GRID LAYOUT IN BOOTSTRAP 3
            'Gymnasium/004/0': 3,  #CREATING A WORDPRESS THEME
            'Gymnasium/100/0': 4, #CODING FOR DESIGNERS
            'Gymnasium/101/0': 5, #RESPONSIVE WEB DESIGN
            'Gymnasium/102/0': 6, #JQUERY BUILDING BLOCKS
            'Gymnasium/103/0': 7, #UX FUNDAMENTALS
            'Gymnasium/104/0': 8 #JAVASCRIPT FOUNDATIONS
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
        failed_user_enrollments = 0
        for csv_file, course_id_str in course_id_mapping.iteritems():
            #  print csv_file + " - " + course_id
            #email = user_info[2]

            with open(csv_file,'rU') as f:
                reader = csv.reader(f)
                data = list(reader)
                #strip off first line column names
                labels = data[0]
                data = data[1:]

                #workflow from lms/djangoapps/instructor/views/api.py:students_update_enrollmen
                #def students_update_enrollment(request, course_id):
                course_name = course_name_mapping[course_id_str]
                section_prefix = course_prefix_mapping[course_id_str]
                course_id = SlashSeparatedCourseKey.from_deprecated_string(course_id_str)
                action = 'enroll'
                # identifiers_raw = request.POST.get('identifiers')
                # identifiers = _split_input_list(identifiers_raw)
                auto_enroll = True
                email_students = False
                email_params = {}
                language = get_user_email_language(None)

                for d in data:
                    course_email = d[0]

                    try:
                        course_email.decode('utf-8')
                    except UnicodeDecodeError:
                        print 'could not add user (bad email): %s' % course_email
                        failed_user_enrollments += 1
                        continue

                    if not course_email in user_actions.keys():
                        user_actions[course_email] = []
                        unique_user_enrollments += 1

                    email = course_email #skipping email validation
  
                    before, after = enroll_email(course_id, email, auto_enroll, email_students, email_params, language=language)

                    #find last completed section
                    indices = [i for i, x in enumerate(d) if x in ["INC", "COMP"] ]
                    try:
                        max_ind = max(indices)
                    except ValueError:
                        #if value not found
                        max_ind = 4

                    last_section = section_prefix + ' ' + labels[max_ind]

					#record actions
                    user_actions[course_email].append({'CourseName': course_name, 'CourseID': course_id_str, 'LastSection': last_section} )
                    total_enrollments += 1

            print 'done with: %s' % csv_file

#0 - first name
#1 - last name
#2 - email
#3 - city
        json_output_data = []
        with open('/opt/course_export/Student_Activity.csv','rU') as f:
            reader = csv.reader(f)
            data = list(reader)
            data = data[1:]


            #for each datapoint in Student_Activity dump
            for d in data:
                first_name = d[0]
                last_name = d[1]
                email = d[2]
                full_name = first_name + ' ' + d[1]
                email = d[2]
                market = d[3]

                course_json = []
                try: 
                    courses = user_actions[email]
                    course_json = [ { 'Course': course['CourseName'], 'CourseID': course['CourseID'], 'LastSection': course['LastSection'] } for course in courses ]
                except KeyError:
                    #user not added to any courses
                    pass

                registration_url = 'thegymnasium.com/register?auto-reg&{query_string}'.format(
                    query_string=urllib.urlencode({'email': email, 'name': full_name, 'market': market})
                )

                output_data = {
                    'Student': {
                        'FirstName': first_name,
                        'LastName': last_name,
                        'Email': email,
                        'Courses': course_json,
                        'RegistrationURL': registration_url
                    }
                }

                json_output_data.append(output_data)


            #print json.dumps(output_data, indent=2)

        # with open('/tmp/dry_run_enrollment_output','wb') as f:
        #     f.write(json.dumps(json_output_data, indent=2))

        #write actions to sample csv file
        output_labels = ['first_name', 'last_name', 'email',
                        'GYM001','GYM002','GYM003','GYM004',
                        'GYM100','GYM101','GYM102','GYM103',
                        'GYM104','registration_url'
            ]
        with open('/tmp/dry_run_enrollment_output.csv','wb') as f:
            f.write('%' + ','.join(output_labels) + '\n')
            for json_data in json_output_data:
                # f.write('%s: %s\n' % (user, ', '.join(actions)))
                user_data = json_data['Student']
                first_name = user_data['FirstName']
                last_name = user_data['LastName']
                email = user_data['Email']
                registration_url = user_data['RegistrationURL']

                courses = user_data['Courses']
                # course_state_list = []
                # for x in range(9):
                #     if x < len(courses):
                #         c = courses[x]
                #         course_state_list.extend([ c['Course'], c['LastSection'] ]) 
                #     else:
                #         course_state_list.extend([ '', '' ])
                course_state_list = [''] * 9
                for course in courses:
                    ind = course_index_mapping[course['CourseID']]
                    course_state_list[ind] = course['LastSection']

                output_row = '{first_name},{last_name},{email},{course_list},{registration_url}\n'.format(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    course_list=','.join(course_state_list),
                    registration_url=registration_url
                )
                f.write(output_row)

        print 'total enrollments: %d' % total_enrollments
        print 'unique users enrolled: %d' % unique_user_enrollments
        print 'user enrollment failures: %d' % failed_user_enrollments

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

