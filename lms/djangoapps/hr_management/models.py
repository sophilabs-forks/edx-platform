from django.db import models

from django.contrib.auth.models import User

from course_modes.models import CourseMode
from xmodule_django.models import CourseKeyField
from organizations.models import Organization

# NOTE: V1 - NYIF admins will be given access to this /admin interface
#            where they wil be able to assign the HrManager role to existing users
#            
class HrManager(models.Model):
    user = models.OneToOneField(User)
    organization = models.OneToOneField(Organization)

    def __str__(self):
        return '{}: {}'.format(self.user, self.organization)
    #organization = models.ManyToManyField(Org)


class CourseAccessRequest(models.Model):
    user = models.ForeignKey(User)
    course_id = CourseKeyField(max_length=255, db_index=True)
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    # Represents the modes that are possible. We'll update this later with a
    # list of possible values.
    mode = models.CharField(default=CourseMode.DEFAULT_MODE_SLUG, max_length=100)

    @classmethod
    def has_requested_access(cls, user, course_key):
        """
        Returns True if the user has requested access to the course. Otherwise, returns False.

        `user` is a Django User object. If it hasn't been saved yet (no `.id`
               attribute), this method will automatically save it before
               adding an enrollment for it.

        `course_id` is our usual course_id string (e.g. "edX/Test101/2013_Fall)
        """
        if not user.is_authenticated():
            return False

        record_exists = CourseAccessRequest.objects.filter(user=user, course_id=course_key).exists()
        return record_exists
