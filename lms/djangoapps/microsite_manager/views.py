import logging
import re
import sys
from urlparse import urlparse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (
	Http404,
	HttpResponse,
	HttpResponseBadRequest,
	HttpResponseForbidden,
	)
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from edxmako.shortcuts import render_to_response
from microsite_configuration.models import Microsite

from .utils import generate_microsite_vo, create_microsite

log = logging.getLogger(__name__)

log.setLevel(logging.INFO)


@login_required
def index(request):
    if not request.user.is_staff:
        raise Http404

    domain = request.META.get('HTTP_HOST', None)
    # domain will be the domain as showin in the browser URL bar
    # ex for localhost: "localhost:8000" or "127.0.0.1:8000"
    log.info("hr-management#index domain = {}".format(domain))

    # Serve up the 'manage microsites page'
    # We don't have to worry about pagination *yet*
    # https://docs.djangoproject.com/en/1.8/topics/pagination/
    url = urlparse(request.build_absolute_uri())

    log.info("Host full url={}".format(url))
    log.info("hostname = {}".format(url.hostname))
    log.info("port = {}".format(url.port))

    # We're making an assumtion that we are in our site TLD (not a microsite url)
    # Because a TLD could be:
    # * localhost
    # * example.com
    # * example.co.uk
    # * learning.nyif.com (where we will have microsites like 
    #   micro1.learning.nyif.com)
    #
    microsites = [
        generate_microsite_vo(obj, url.port) for obj in Microsite.objects.all().order_by('key')
    ]

    context = {
        'message': 'manage microsites',
        'user': request.user,
        'microsites': microsites,
        'hostname': url.hostname,
    }

    return render_to_response('microsite_manager/index.html', context) 

# TODO: We need to set proper authorizataion for this call
@login_required
@require_POST
def add_microsite(request):
    domain=request.POST.get('hostname')
    org_long_name=request.POST.get('org_long_name')
    org_short_name=request.POST.get('org_short_name')
    org_description=request.POST.get('org_description')
    subdomain_name=request.POST.get('subdomain_name')

    all_valid = True
    slug_re = re.compile("^[A-Za-z0-9-_]+$")

    if org_long_name is None or org_long_name.strip() == '':
        messages.error(request, "Organization long name cannot be empty")
        all_valid = False
    if not slug_re.match(org_short_name):
        messages.error(request,
            "Organization short name '{}' is not valid. ".format(org_short_name))
        all_valid = False
    if not slug_re.match(subdomain_name):
        messages.error(request,
            "Subdomain name '{}' is not valid. ".format(subdomain_name))
        all_valid = False

    user = request.user

    if all_valid:
        try:
            data = create_microsite(
                domain=domain,
                org_long_name=org_long_name,
                org_short_name=org_short_name,
                org_description=org_description,
                subdomain_name=subdomain_name,
            )
            messages.info(request, "Microsite {} succesfully created".format(data.key))
        except:
            e = sys.exc_info()[0]
            messages.error(request, "Error creating microsite: {}".format(e))

    # TODO: Help the user by passing variables back to template. Maybe Django
    # Forms does this automatically
    return redirect('index')

