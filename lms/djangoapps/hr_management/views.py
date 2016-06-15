import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden)
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from ipware.ip import get_ip
from opaque_keys import InvalidKeyError
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from organizations.models import Organization

from course_modes.models import CourseMode
from embargo import api as embargo_api
from microsite_configuration.models import Microsite
from student.models import CourseEnrollment
from util.db import outer_atomic
from xmodule.modulestore.django import modulestore
from .models import HrManager, CourseAccessRequest

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
    return render(request, 'hr_management/index.html',context)

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

    context = {
        'message': 'hr user list',
        'user': user,
        'microsite': microsite,
        'organization': organization,
        'users': users
    }
    return render(request, 'hr_management/users.html',context)

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
    return render(request, 'hr_management/courses.html',context)

#TODO: refactor into decorator/mixin
def _user_has_access(user,organization):
    '''
    set user access in /admin/hr_management/hrmanager/
    '''
    user_exists = HrManager.objects.filter(user__username=user).filter(organization__short_name=organization)

    if user_exists:
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
                CourseAccessRequest.objects.get_or_create(
                    user=user,
                    course_id=course_id,
                    mode=enroll_mode
                )
        except Exception:
            return HttpResponseBadRequest(_("Could not request access"))

        return HttpResponse()
        return HttpResponse(reverse('about_course', kwargs={'course_id': course_id.to_deprecated_string()}))
    else:
        return HttpResponseBadRequest(_("Enrollment action is invalid"))
