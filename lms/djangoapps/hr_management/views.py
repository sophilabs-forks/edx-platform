import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden)
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from ipware.ip import get_ip
from opaque_keys import InvalidKeyError
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from organizations.models import Organization

from course_modes.models import CourseMode
from courseware.courses import get_course_by_id
from edxmako.shortcuts import render_to_string
from embargo import api as embargo_api
from edxmako.shortcuts import render_to_response
from microsite_configuration import microsite
from microsite_configuration.models import Microsite
from student.models import CourseEnrollment
from util.db import outer_atomic
from xmodule.modulestore.django import modulestore
from .models import HrManager, CourseAccessRequest, CourseCCASettings
from hr_management.tasks import send_email_to_user

log = logging.getLogger(__name__)

@login_required
def index(request):
    user = request.user
    domain = request.META.get('HTTP_HOST', None)
    microsite = Microsite.get_microsite_for_domain(domain)
    organizations = microsite.get_organizations()
    organization = organizations[0]

    _user_has_access(user,organization)

    context = {
        'message': 'hr index',
        'user': user,
        'microsite': microsite,
        'organization': organization
    }
    return render_to_response('hr_management/index.html', context)

@login_required
def user_list(request):
    #get all users belonging to specific Org
    user = request.user
    domain = request.META.get('HTTP_HOST', None)
    microsite = Microsite.get_microsite_for_domain(domain)
    organizations = microsite.get_organizations()
    organization = organizations[0]

    _user_has_access(user,organization)

    users = Organization.objects.get(short_name=organization).users.all()
    active_users = [ u for u in users if u.userorganizationmapping_set.get(organization__short_name=organization).is_active ]
    inactive_users = [ u for u in users if not u.userorganizationmapping_set.get(organization__short_name=organization).is_active ]

    context = { 
        'message': 'hr user list',
        'user': user,
        'microsite': microsite,
        'organization': organization,
        'active_users': active_users,
        'inactive_users': inactive_users
    }   

    return render_to_response('hr_management/users.html', context)

@login_required
@require_POST
def change_user_access(request):
    try:
        user_request_object = User.objects.get(id=request.POST.get('user_request_id'))
    except CourseAccessRequest.DoesNotExist:
        return redirect('course_list')

    domain = request.META.get('HTTP_HOST', None)
    microsite = Microsite.get_microsite_for_domain(domain)
    organizations = microsite.get_organizations()
    organization = organizations[0]
    org_mapping = user_request_object.userorganizationmapping_set.get(organization__short_name=organization)

    action = request.POST.get('approve', '') or request.POST.get('reject', '') or request.POST.get('revoke','')
    if action.lower() == 'approve':
        org_mapping.is_active = True
        org_mapping.save()
        messages.success(request, 'Succesfully approved access to user {}'.format(user_request_object.email))
        _send_microsite_request_approved_email_to_user(user_request_object,domain)
    elif action.lower() == 'reject':
        org_mapping.delete()
        messages.success(request, 'Succesfully denied access to user {}'.format(user_request_object.email))
        #TODO send email
    elif action.lower() == 'revoke access':
        #TODO send email
        org_mapping.is_active = False
        org_mapping.save()
        messages.success(request, 'Succesfully revoked access from user {}'.format(user_request_object.email))
        # _send_course_request_approved_email_to_user(access_request.user, access_request.course_id)
    return redirect('user_list')

@login_required
def course_list(request):
    user = request.user
    domain = request.META.get('HTTP_HOST', None)
    microsite = Microsite.get_microsite_for_domain(domain)
    organizations = microsite.get_organizations()
    organization = organizations[0]

    _user_has_access(user,organization)

    courses = [c for c in modulestore().get_courses() if c.org == organization]

    context = {
        'message': 'hr course list',
        'user': user,
        'microsite': microsite,
        'organization': organization,
        'courses': courses
    }
    return render_to_response('hr_management/courses.html', context)


@login_required
def course_detail(request, course_id):
    user = request.user
    domain = request.META.get('HTTP_HOST', None)
    microsite = Microsite.get_microsite_for_domain(domain)
    organizations = microsite.get_organizations()
    organization = organizations[0]

    _user_has_access(user,organization)

    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)

    if course_key.org != organization:
        raise PermissionDenied("That course doesn't belong to this organization")

    course = get_course_by_id(course_key)
    course_requests = CourseAccessRequest.objects.filter(course_id=course_key)
    cca_settings, created = CourseCCASettings.objects.get_or_create(course_id=course_key)

    context = {
        'message': 'hr course list',
        'user': user,
        'microsite': microsite,
        'organization': organization,
        'course': course,
        'course_requests': course_requests,
        'require_access_request': cca_settings.require_access_request,
    }
    return render_to_response('hr_management/course.html', context)



#TODO: refactor into decorator/mixin
#
#This method is meant to limit access of the hr-management pages to
#   only those given access, or superusers
def _user_has_access(user,organization):
    '''
    set user access in /admin/hr_management/hrmanager/
    '''
    user_exists = HrManager.objects.filter(user__username=user).filter(organization__short_name=organization)

    if user.is_superuser or user.is_staff or user_exists:
        return True
    else:
        log.error('User {} does not have access to hr-management for microsite: {}'.format(user, organization))
        raise PermissionDenied


@transaction.non_atomic_requests
@require_POST
@outer_atomic(read_committed=True)
def require_course_access(request, check_access=True):
    # Get the user
    user = request.user

    domain = request.META.get('HTTP_HOST', None)
    microsite = Microsite.get_microsite_for_domain(domain)
    organizations = microsite.get_organizations()
    organization = organizations[0]

    # Ensure the user is authenticated
    if not user.is_authenticated():
        return HttpResponseForbidden()

    # Ensure we received a course_id
    action = request.POST.get("enrollment_action")
    if 'course_id' not in request.POST:
        return HttpResponseBadRequest(_("Course id not specified"))

    try:
        course_id = SlashSeparatedCourseKey.from_deprecated_string(request.POST.get("course_id"))
    except InvalidKeyError:
        log.warning(
            u"User %s tried to %s with invalid course id: %s",
            user.username,
            action,
            request.POST.get("course_id"),
        )
        return HttpResponseBadRequest(_("Invalid course id"))

    if action == "request_access":
        # Make sure the course exists
        # We don't do this check on unenroll, or a bad course id can't be unenrolled from
        if not modulestore().has_course(course_id):
            log.warning(
                u"User %s tried to enroll in non-existent course %s",
                user.username,
                course_id
            )
            return HttpResponseBadRequest(_("Course id is invalid"))

        available_modes = CourseMode.modes_for_course_dict(course_id)

        # Check whether the user is blocked from enrolling in this course
        # This can occur if the user's IP is on a global blacklist
        # or if the user is enrolling in a country in which the course
        # is not available.
        redirect_url = embargo_api.redirect_if_blocked(
            course_id, user=user, ip_address=get_ip(request),
            url=request.path
        )
        if redirect_url:
            return HttpResponse(redirect_url)

        try:
            enroll_mode = CourseMode.auto_enroll_mode(course_id, available_modes)
            if enroll_mode:
                access_request, created = CourseAccessRequest.objects.get_or_create(
                    user=user,
                    course_id=course_id,
                    mode=enroll_mode
                )
                _send_course_request_email_to_managers(access_request.user, access_request.course_id, organization)
        except Exception:
            return HttpResponseBadRequest(_("Could not request access"))

        return HttpResponse(reverse('about_course', kwargs={'course_id': course_id.to_deprecated_string()}))
    else:
        return HttpResponseBadRequest(_("Enrollment action is invalid"))


@login_required
@require_POST
def change_course_access(request):
    try:
        access_request = CourseAccessRequest.objects.get(id=request.POST.get('request_access_id'))
    except CourseAccessRequest.DoesNotExist:
        return redirect('course_list')

    action = request.POST.get('approve', '') or request.POST.get('reject', '')
    course_id = access_request.course_id
    if action.lower() == 'approve':
        CourseEnrollment.enroll(access_request.user, access_request.course_id, access_request.mode)
        messages.success(request, 'Succesfully approved access to {} for {}'.format(
            access_request.course_id, access_request.user.email))
        access_request.delete()
        _send_course_request_approved_email_to_user(access_request.user, access_request.course_id)
    elif action.lower() == 'reject':
        access_request.delete()
        messages.success(request, 'Succesfully denied access to {} for {}'.format(
            access_request.course_id, access_request.user.email))
    return redirect('course_detail', course_id=course_id.to_deprecated_string())


@login_required
@require_POST
def change_course_cca_settings(request):
    course_id = request.POST.get('course_id')
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    cca_settings = CourseCCASettings.objects.get(course_id=course_key)
    require_access_request = (request.POST.get('require_access_request', '').lower() == 'on')
    cca_settings.require_access_request = require_access_request
    cca_settings.save()
    messages.success(request, 'Succesfully updated course settings')
    return redirect('course_detail', course_id=cca_settings.course_id.to_deprecated_string())

def send_microsite_request_email_to_managers(request, user):
    domain = request.META.get('HTTP_HOST', None)
    microsite_object = Microsite.get_microsite_for_domain(domain)
    organizations = microsite_object.get_organizations()
    organization = organizations[0]

    context = {
        'user': user,
        'domain': domain
    }
    subject = render_to_string('hr_management/emails/microsite_access_requested_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('hr_management/emails/microsite_access_requested.txt', context)

    from_address = microsite.get_value(
        'email_from_address',
        settings.DEFAULT_FROM_EMAIL
    )
    try:
        hr_managers_emails = HrManager.objects.filter(organization__short_name=organization).values_list('user__email', flat=True)
        send_email_to_user.delay(subject, message, from_address, list(hr_managers_emails))
    except Exception:  # pylint: disable=broad-except
        log.error(u'Unable to send course request approved email to user from "%s"', from_address, exc_info=True)

def _send_microsite_request_approved_email_to_user(user, domain):
    context = {
        'user': user,
        'domain': domain,
    }
    subject = render_to_string('hr_management/emails/microsite_request_approved_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('hr_management/emails/microsite_request_approved.txt', context)

    from_address = microsite.get_value(
        'email_from_address',
        settings.DEFAULT_FROM_EMAIL
    )
    try:
        send_email_to_user.delay(subject, message, from_address, [user.email])
    except Exception:  # pylint: disable=broad-except
        log.error(u'Unable to send course request approved email to user from "%s"', from_address, exc_info=True)

def _send_course_request_email_to_managers(user, course_id, organization):
    course = get_course_by_id(course_id)
    context = {
        'user': user,
        'course_name': course.display_name,
    }
    subject = render_to_string('hr_management/emails/course_access_requested_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('hr_management/emails/course_access_requested.txt', context)

    from_address = microsite.get_value(
        'email_from_address',
        settings.DEFAULT_FROM_EMAIL
    )
    try:
        hr_managers_emails = HrManager.objects.filter(organization__short_name=organization).values_list('user__email', flat=True)
        send_email_to_user.delay(subject, message, from_address, list(hr_managers_emails))
    except Exception:  # pylint: disable=broad-except
        log.error(u'Unable to send course request approved email to user from "%s"', from_address, exc_info=True)


def _send_course_request_approved_email_to_user(user, course_id):
    course = get_course_by_id(course_id)
    context = {
        'user': user,
        'course_name': course.display_name,
    }
    subject = render_to_string('hr_management/emails/course_request_approved_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('hr_management/emails/course_request_approved.txt', context)

    from_address = microsite.get_value(
        'email_from_address',
        settings.DEFAULT_FROM_EMAIL
    )
    try:
        send_email_to_user.delay(subject, message, from_address, [user.email])
    except Exception:  # pylint: disable=broad-except
        log.error(u'Unable to send course request approved email to user from "%s"', from_address, exc_info=True)
