
import csv
import logging

from certificates.models import CertificateWhitelist
from django.contrib.auth.models import User
from django.conf import settings

from accredible_certificate.queue import CertificateGeneration

from opaque_keys.edx.locations import SlashSeparatedCourseKey

# log = logging.getLogger(__name__)

#column in the CSV corresponding to course status
course_index_mapping = { 
    'GYM/001/0': 3, #DEFEATING BUSY
    'GYM/002/0': 4, #INTRODUCING NODE.JS
    'GYM/003/0': 5, #GRID LAYOUT IN BOOTSTRAP 3
    'GYM/004/0': 6,  #CREATING A WORDPRESS THEME
    'GYM/100/0': 7, #CODING FOR DESIGNERS
    'GYM/101/0': 8, #RESPONSIVE WEB DESIGN
    'GYM/102/0': 9, #JQUERY BUILDING BLOCKS
    'GYM/103/0': 10, #UX FUNDAMENTALS
    'GYM/104/0': 11 #JAVASCRIPT FOUNDATIONS
}

migration_data_csv = '/opt/course_export/final_migration_enrollment_output.csv'

def generate_student_certificates(user):
    fid = open(migration_data_csv,'rU')
    reader = csv.reader(fid)
    data = list(reader)
    data = data[1:] #remove label header

    #find user in csv
    student_row = None
    for d in data:
        if user.email in d:
            student_row = d
            break

    if not student_row:
        # log.error('Could not find student email: {} in migration csv file. If they are a new student, this is expected'.format(user.email))
        return
    
    cg = CertificateGeneration(api_key=settings.APPSEMBLER_FEATURES['ACCREDIBLE_API_KEY'])
    for course_key, index in course_index_mapping.iteritems():

        if 'Certified' in student_row[index]:
            course_id = SlashSeparatedCourseKey.from_deprecated_string(course_key)

            #check db for whiltelist 
            cw = CertificateWhitelist.objects.filter(user=user).filter(course_id=course_id)

            #if no whitlelist, add to list and generate cert
            if not cw:
                cw = CertificateWhitelist(user=user, course_id=course_id, whitelist=True)
                cw.save()

                try:
                    cg.add_cert(user,course_id,forced_grade='pass')
                    # log.log('added cert for user: %s, course: %s' % (user.username, str(course_id)))
                except:
                    # log.log('could not create cert for user: %s for course: %s' % (user.username, str(course_id)))
                    pass

#turn into management cmd at some point
def generate_certs_existing_students():
    for user in User.objects.all():
        generate_student_certificates(user)
