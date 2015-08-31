from django.core.management.base import BaseCommand

from xmodule.modulestore.django import modulestore

from course_access_group.models import CourseStub

#this is only temporary
#turn this into cron job to run nightly and keep dbs up to date with each other
#TODO: handle courses being deleted from mongo
class Command(BaseCommand):
    help = """Sync courses in Mongo with CourseStub objects in MySQL."""

    def handle(self, *args, **options):
        update_count = 0

        mongo_courses = modulestore().get_courses()
        #mysql_courses = CourseStub.objects.all()

        for course in mongo_courses:
            course_id = course.id
            course_name = course.display_name

            if not CourseStub.objects.filter(course_id=course_id):
                cs = CourseStub(name=course_name, course_id=course_id)
                cs.save()

                update_count += 1

        print 'Updated %d records' % update_count

        if len(mongo_courses) != len(CourseStub.objects.all()):
            print 'Warning: DBs out of sync:'
            print 'Mongo: %d courses' % len(mongo_courses)
            print 'MySQL: %d courses' % len(CourseStub.objects.all())