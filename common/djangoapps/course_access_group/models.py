from django.db import models

#from student.models import ...
from django.contrib.auth.models import User

from xmodule_django.models import CourseKeyField

#come up with better way of handling this
#one to one relationship with Courses in mongodb
class CourseStub(models.Model):
	name = models.CharField(default='', max_length=255)
	#course_id = models.CharField(default='', max_length=255, unique=True)
	course_id = CourseKeyField(default='', max_length=255, unique=True)

	def __str__(self):
		return self.course_id

class CourseAccessGroup(models.Model):
	name = models.CharField(default='', max_length=32)
	#figure out whether to use UserProfile or User object
	students = models.ManyToManyField(User)
	courses = models.ManyToManyField(CourseStub, blank=True)

	def __str__(self):
		return self.name

