# Bulk Enrollment API

## Authentication
The API requires OAuth authentication to grant access to the endpoints and actions.

All endpoint can return the following response errors if there some problem with the authentication process:

### Credentials not provided
* Code: 401 UNAUTHORIZED
* Content: `{ detail : "Authentication credentials were not provided." }`
* Reason: Authentication credentials were not provided.

### Invalid Token
* Code: 401 UNAUTHORIZED
* Content: `{ detail : "Invalid Token." }`
* Reason: Invalid OAuth Token.

## Bulk Enrollment

Endpoint that allows you to enroll or unenroll multiple students into/out of multiple courses with
optional email notification.

* URL: `/appsembler/bulk_enroll/`
* Method: `POST`
* Data Params
	* Required:
		* action ( 'enroll' or 'unenroll' )
		* identifiers (comma separated list of student emails, example: `test_user@appsembler.com,another_user@appsembler.com` )
		* courses (comma separated list of student emails, example:
`course-v1:edX+DemoX+Demo_Course,course-v1:Appsembler+APP101+1Q2016` )
	* Optional:
		* auto_enroll (boolean, defaults to false )
		* email_students (boolean, defaults to false )

* Success Response:
	* Code: 200
	* Content:
	```
	{
	"action": "unenroll",
	"courses": {
		"course-v1:edX+DemoX+Demo_Course": {
			"action": "unenroll",
			"results": [{
				"identifier": "test@appsembler.com",
				"after": {
					"enrollment": false,
					"allowed": false,
					"user": true,
					"auto_enroll": false
				},
				"before": {
					"enrollment": false,
					"allowed": false,
					"user": true,
					"auto_enroll": false
				}
			}],
			"auto_enroll": true
		}
	},
	"email_students": false,
	"auto_enroll": true
}
	```

* Error Response: I
	* Code: 401 UNAUTHORIZED
	* Content: { detail : "Authentication credentials were not provided." }
	* Reason: Missing or incorrect auth credentials
**OR**
	* Code: 404 NOT FOUND
	* Content: { detail : "Not found" }
	* Reason: Wrong course ID
**OR**
	* Code: 400 BAD REQUEST
	* Content: {"identifiers": ["This field is required."]}
	* Reason: Missing a required field

* Sample Call:
```
POST /appsembler/bulk_enroll/ HTTP/1.1
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5da152cf6a4833c957d882ee1624c954b86
Cache-Control: no-cache
{
	"action": "enroll",
	"auto_enroll": true,
	"identifiers": "test@appsembler.com,test1@appsembler.com,test2@appsembler.
	com ",
	"email_students": true,
	"courses": "course-v1:edX+DemoX+Demo_Course,course-v1:Appsembler+APP101+1Q
	2016 "
}
```
