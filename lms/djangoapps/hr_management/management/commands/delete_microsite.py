
import argparse
import os

from django.core.management.base import BaseCommand, CommandError

from django.contrib.sites.models import Site

from microsite_configuration.models import Microsite, MicrositeOrganizationMapping
from organizations import api as orgsApi

"""
Tables

django_site
organizations_organizationmicrosite_configuration_microsite

microsite_configuration_microsite
microsite_configuration_micrositehistory
microsite_configuration_micrositeorganizationmapping

organizations_organization
organizations_organizationcourse
organizations_userorganizationmapping

truncate table X
or

delete from table X;

ALTER TABLE mytable AUTO_INCREMENT = 1

"""

class Command(BaseCommand):
    help = 'delete the specified microsite'

    def add_arguments(self, parser):
        parser.add_argument('microsite', nargs='+', type=str)

    def handle(self, *args, **options):
        for microsite in options['microsite']:
            try:
                microsite = Microsite.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('microsite')
    args = parser.parse_args()

    print("microsite={}".format(args.microsite))

    

if __name__ == '__main__':
    main()

