from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from course_access_group.models import CourseAccessGroup
from salesforce_registration.models import SalesforceDomainEntry

from simple_salesforce import Salesforce

#turn this into cron job to run nightly and the results cached
#TODO: handle courses being deleted from salesforce
class Command(BaseCommand):
    help = """Categorize users into CourseAccessGroup based on email domain."""

    def handle(self, *args, **options):
        update_count = 0
        unchanged_count = 0
        not_categorized = 0

        categories = ['Employee', 'Partner', 'Customer']

        for category in categories:
            users = User.objects.all()

            for user in users:
                email_domain = user.email.split('@')[1]

                salesforce_domain_entry = SalesforceDomainEntry.objects.filter(domain=email_domain)
                if not salesforce_domain_entry:
                    not_categorized += 1
                    continue

                salesforce_category = salesforce_domain_entry[0].category #assuming only one entry in list

                #user_groups = CourseAccessGroup.objects.filter(students__username=user.username)
                

                #only add additional groups
                access_group = CourseAccessGroup.objects.get(name=salesforce_category)
                user.courseaccessgroup_set.add(access_group)

                update_count += 1

                


        print 'Updated %d user CourseAccessGroup domain entries' % update_count
        print 'Unchanged: %d users' % unchanged_count
        print 'Not categorized: %d users' % not_categorized
