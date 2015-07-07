import logging

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt                                          
from django.contrib.auth.models import User
from django.core.validators import validate_email

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from courseware.courses import get_course_by_id
from instructor.enrollment import (
    enroll_email,
    get_email_params,
)


logger = logging.getLogger(__name__)

@csrf_exempt 
def endpoint(request):
    if request.method != 'POST':
        logger.warning('Non-POST request coming to url: /infusionsoft')
        raise Http404

    post_secret = request.POST.get('SecretKey','')
    server_secret = settings.APPSEMBLER_FEATURES.get('INFUSIONSOFT_SECRET_KEY','')
    if post_secret != server_secret:
        msg = "POST request from Infusionsoft failed with secret key: {}".format(post_secret)
        logger.error(msg)
        return HttpResponse(status=403)

    course_id_str = request.POST.get('CourseId','')
    if not course_id_str:
        logger.error('Could not extract CourseId from POST request')
        return HttpResponse(status=400)

    user_email = request.POST.get('Email','')
    if not user_email:
        logger.error('Could not extract Email from POST request')
        return HttpResponse(status=400)

    ##based on students_update_enrollment() in  djangoapps/instructor/views/api.py
    course_id = SlashSeparatedCourseKey.from_deprecated_string(course_id_str)
    action = 'enroll'
    auto_enroll = True
    email_students = True

    email_params = {} 
    if email_students:
        course = get_course_by_id(course_id)
        email_params = get_email_params(course, auto_enroll, secure=request.is_secure())

    # First try to get a user object based on email address
    user = None 
    email = None 
    # language = None 
    try: 
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        email = user_email
    else:
        email = user.email
        # language = get_user_email_language(user)

    try: 
        # Use django.core.validators.validate_email to check email address
        # validity (obviously, cannot check if email actually /exists/,
        # simply that it is plausibly valid)
        validate_email(email)  # Raises ValidationError if invalid

        if action == 'enroll':
            before, after = enroll_email(
                course_id, email, auto_enroll, email_students, email_params 
            )

    except ValidationError:
        # Flag this email as an error if invalid, but continue checking
        # the remaining in the list
        logger.error('User email did not validate correctly: {}'.format(email))
        return HttpResponse(status=400)

    except Exception as exc:  # pylint: disable=broad-except
        # catch and log any exceptions
        # so that one error doesn't cause a 500.
        log.exception("Error while #{}ing student")
        log.exception(exc)
        return HttpResponse(status=400)
        

    return HttpResponse(status=200)

