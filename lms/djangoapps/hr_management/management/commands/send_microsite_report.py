"""
Email microsite report to specified hr managers 
"""
from textwrap import dedent

from django.core.management.base import BaseCommand

from hr_management.tasks import generate_and_email_customer_report


class Command(BaseCommand):
    """
    Generate microsite report and email to specified hr managers
    """
    args = ""
    help = dedent(__doc__).strip()

    def handle(self, *args, **options):
        generate_and_email_customer_report()
