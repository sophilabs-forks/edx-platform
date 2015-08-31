from django.db import models

#from student.models import ...
from django.contrib.auth.models import User

from xmodule_django.models import CourseKeyField

class CourseAccessGroup(models.Model):
	name = models.CharField(default='', max_length=32)
	#figure out whether to use UserProfile or User object
	students = models.ManyToManyField(User)
	#courses = models.ManyToManyField(CourseKeyField)
	#courses = models.CharField(max_length=32)

	def __str__(self):
		return self.name
