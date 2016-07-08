from hr_management.models import CourseAccessRequest


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
