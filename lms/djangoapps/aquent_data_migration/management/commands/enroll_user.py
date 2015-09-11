#!/usr/bin/python
"""
django management command: create single user based on CSV string
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test CSV import capabilities for single user"

    def handle(self, *args, **options):

        print "args = ", args


