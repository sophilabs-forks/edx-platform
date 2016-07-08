from smtplib import SMTPException

from celery.task import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail


LOGGER = get_task_logger(__name__)


@task()
def send_email_to_user(subject, message, from_address, email_addresses):
    """ Updates course search index. """
    for email in email_addresses:
        try:
            send_mail(subject, message, from_address, [email])
        except SMTPException as exc:
            LOGGER.error('Error sending email to {}'.format(email))
        else:
            LOGGER.debug('Successfully sent email to {}'.format(email))
