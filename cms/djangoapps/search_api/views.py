
import json
 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from opaque_keys import InvalidKeyError

from . import api

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
@require_POST
def reindex_course(request):
	"""

	"""
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
		return HttpResponse(json.dumps(response_data), status=200)
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
