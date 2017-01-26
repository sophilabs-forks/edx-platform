
import json
 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from opaque_keys import InvalidKeyError

from . import api

# TODO: get this from settings
ALLOWED_ORIGIN = '*'

description = """
Appembler Open edX search api. 

Opens up access to Open edX'sa search infrastructure via HTTP (REST) API interfaces.

"""

@csrf_exempt
def index(request):
    return HttpResponse(json.dumps({
            'description': description,
        })
    )

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def reindex_course(request):
    """

    """
    if request.method == 'POST':
        request_data = json.loads(request.body)
        course_id = request_data.get('course_id')
        try:
            results = api.reindex_course(course_id)
            response_data = {
                'course_id': course_id,
                'status': 'OK',
                'message': 'course reindex initiaated',
                'results': results,
            }
            response = HttpResponse(json.dumps(response_data),
                content_type='application/json',
                status=200)
            response['Access-Control-Allow-Origin'] = ALLOWED_ORIGIN
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = '*'
            return response
        except Exception as e:
            if isinstance(e, InvalidKeyError):
                message = 'InvalidKeyError: Cannot find key for course string ' + \
                    '"{}"'.format(course_id)
                status = 400
            else:
                message = 'Exception "{}" msg: {}'.format(e.__class__, e.message)
                status = 500
            return HttpResponse(json.dumps({
                    'course_id': course_id,
                    'status': 'ERROR',
                    'message': message,
                }), status=status)
    elif request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = ALLOWED_ORIGIN
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        # Options do not allow wildcard for access-control-allow-headers
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    else:
        # Shouldn't get here because of the "require" decorator
        return HttpResponse(json.dumps({
            'status': 'ERROR',
            'msg': 'unsupported request method:{}'.format(request.method)
            }), status=500)
