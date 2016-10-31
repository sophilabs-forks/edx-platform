
# Standard Python includes
from collections import namedtuple
from datetime import datetime
import csv
import io
import logging

# Django includes
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

# Open edx includes
from courseware.courses import get_course_by_id
from instructor.offline_gradecalc import student_grades
from instructor.utils import DummyRequest
from microsite_configuration.models import Microsite, MicrositeOrganizationMapping
from organizations import api as orgsApi
from student.models import CourseEnrollment

# other 3rd party includes

# this package includes

from hr_management.models import CourseAccessRequest



log = logging.getLogger(__name__)

log.setLevel(logging.INFO)


HrefLabel = namedtuple('HrefLabel', ['href', 'label'])

# Microsite value object. Primary use in templates
# the url members are intended for the HrefLabel above
MicrositeVO = namedtuple('MicrositeVO', ['home_url', 'management_url', 'microsite'])

def requested_access_for_course(course, user):
    """
    Return True if user is registered for course, else False
    """
    if user is None:
        return False
    if user.is_authenticated():
        return CourseAccessRequest.has_requested_access(user, course.id)
    else:
        return False

def generate_csv_grade_string(organization=None):
    """
    Create a CSV string that will be included in weekly report email
    """
    header = ['#full_name','email','organization','course_name','enrollment_date','progress','completion_date','score']
    encoded_header = [unicode(s).encode('utf-8') for s in header ]
    fp = io.BytesIO()
    writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(encoded_header)

    if not organization:
        student_list = User.objects.all()
    else:
        student_list = User.objects.filter(organizations__short_name=organization)

    request = DummyRequest()

    output_data = []
    for student in student_list:
        try:
            full_name = student.profile.name
        except: 
            continue
        try: 
            organization = student.organizations.all()[0]
        except: 
            organization = 'none'

        email = student.email
        for enrollment in student.courseenrollment_set.all(): 
            try:
                course = get_course_by_id(enrollment.course_id)
            except: 
                continue
            grade = student_grades(student, request, course)
            enrollment_date = enrollment.created
            course_name = course.display_name
            progress = ''
            completion_date = ''
            score = grade['percent']
            row = [
                full_name,
                email,
                organization,
                course_name,
                enrollment_date,
                progress,
                completion_date,
                score
            ]
            encoded_row = [unicode(s).encode('utf-8') for s in row]
            writer.writerow(encoded_row)

    raw_grade_data = fp.getvalue()
    fp.close()

    return raw_grade_data

def generate_microsite_vo(microsite, port=None):
    """
    Create a namedtuple of data to show in the UI

    We build our urls here to keep the view and template simpler

    Massage microsites to get the urls we want
    Use protocol relative URL

    Perhaps another option is creating custom template filters
    https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/
    """
    port_str = ':{}'.format(port) if port else ''
    return MicrositeVO(
        home_url=HrefLabel(
            href='//{}{}'.format(microsite.site.domain, port_str),
            label=microsite.site),
        management_url=HrefLabel(
            href='//{}{}/hr-management/'.format(microsite.site.domain, port_str),
            label='manage'),
        microsite=microsite
    )

def create_microsite(**kwargs):
    """

    Example of end result:
    Site: 
    domain name: fdic.learning.nyif.com
    display name: fdic

    Organization:
    long name: 'FDIC'
    short name: 'FDIC'
    Description: 'fdic microsite'


    microsite:
        Site: fdic.learninbg.nyif.com
        key: 'fdic'
        values: {
      "PLATFORM_NAME":"FDIC",
      "platform_name":"FDIC"
    }

        TODO: Add testing when data broken (like missing org_long_name)
    """

    # Do some sanity checking
    # TODO: Raise if missing critical data

    log.info("create_microsite kwargs = {}".format(kwargs))

    subdomain_name = kwargs.get('subdomain_name')
    # first check if microsite exists
    microsites = Microsite.objects.filter(key=subdomain_name)
    if microsites:
        return microsites[0]

    subdomain_full_hostname = "{}.{}".format(
        kwargs.get('subdomain_name'),
        kwargs.get('domain')
    )

    try:
        organization = orgsApi.get_organization_by_short_name(
            kwargs.get('org_short_name'))
        # TODO: Also need to check org by long name
    except:
        organization = None

    if not organization:
        organization = orgsApi.add_organization({
            'name': kwargs.get('org_long_name'),
            'short_name': kwargs.get('org_short_name'),
            'description': kwargs.get('org_description')
            });

    # TODO: Check if site already exists
    sites = Site.objects.filter(domain=subdomain_full_hostname)
    if sites:
        site = sites[0]
    else:
        site = Site(domain=subdomain_full_hostname, name=subdomain_name)
        site.save()

    # We're just being consistent with NYIF's existing microsite for this one
    platform_name = subdomain_name.upper()   

    microsite = Microsite(
        key=subdomain_name.lower(),
        values={
            'PLATFORM_NAME': platform_name,
            'platform_name': platform_name
        },
        site=site)
    microsite.save()
    # TODO: Double check if we are using long or short name
    morg = MicrositeOrganizationMapping(microsite=microsite,
        organization=kwargs.get('org_short_name'))
    morg.save()
    
    return microsite

def delete_microsite(microsite):
    '''
    Deletes the given microsite and mapping to organization
    :param Microsite microsite: The microsite to delete
    :return: True if microsite deleted False if not

    TODO: Consider passing the microsite name (key is the field name) to this
    method and move the code in the `Command` handle method to here
    And add testing
    TODO: Add flag to delete org and/or site
    '''

    if not microsite:
        return False
    else:
        # Get the mapping
        mapping_qs = MicrositeOrganizationMapping.objects.filter(
            microsite=microsite.id)
        if mapping_qs.count() == 1:
            mapping_qs[0].delete()
        else:
            # found none or more than one (bad state for the lastter)
            return False

        microsite.delete()
        # at this point just assuming we've deleted it
        # TODO: Add exception handling for delete failure?
        return True
