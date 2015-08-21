from django.db import models

#from student.models import ...
from django.contrib.auth.models import User

from xmodule_django.models import CourseKeyField

class CourseAccessGroup(models.Model):
	#figure out whether to use UserProfile or User object
	students = models.ManyToManyField(User)
	#courses = models.ManyToManyField(CourseKeyField)

