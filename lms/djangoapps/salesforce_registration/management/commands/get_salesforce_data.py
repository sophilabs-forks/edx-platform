from django.conf import settings
from django.core.management.base import BaseCommand

from salesforce_registration.models import SalesforceDomainEntry

from simple_salesforce import Salesforce

#turn this into cron job to run nightly and the results cached
#TODO: handle courses being deleted from salesforce
class Command(BaseCommand):
    help = """Sync columns from Salesforce Partner/Customer columns with MySQL."""

    def handle(self, *args, **options):
        update_count = 0

    username = settings.APPSEMBLER_FEATURES['SALESFORCE_USERNAME']
    password = settings.APPSEMBLER_FEATURES['SALESFORCE_PASSWORD']
    token = settings.APPSEMBLER_FEATURES['SALESFORCE_TOKEN']

    sf = Salesforce(password=password, username=username, security_token=token)
    

    categories = ['Partner', 'Customer']

    for category in categories:
        query_result = sf.query("SELECT Email_Domain__c FROM Account WHERE Type='{}'".format(category)) 

        records = query_result['records']
        for record in records:
            entry = SalesforceDomainEntry.objects.filter(domain=record)

            if not entry:
                entry = SalesforceDomainEntry(domain=record, category=category)
                entry.save()

                update_count += 1

    print 'Updated %d Salesforce domain entries' % update_count
