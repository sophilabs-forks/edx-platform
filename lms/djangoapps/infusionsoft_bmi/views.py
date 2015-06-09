import logging

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt                                          

from edxmako.shortcuts import render_to_response
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

post_fields = ['contactId','task','FirstName','LastName','Email','StudentId']

@csrf_exempt 
def endpoint(request):
    # if request.method != 'POST':
    #   raise Http404

    for p in post_fields:
        #print p + ' ' + request.POST.get(p)
        logger.info(p + ' ' + request.POST.get(p))
        # print p

    # request.POST.get('contactId')



    User.objects.filter(email=request.POST.get('Email'))
    #if student exists on the site already

    #if student doesn't exist

    return HttpResponse(status=200)
