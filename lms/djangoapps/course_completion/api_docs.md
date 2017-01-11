# Course Completion API Endpoint

## Authentication
The API requires OAuth authentication to grant access to the endpoints and actions.

All endpoints can return the following response errors if there are problems with the authentication process:

### Credentials not provided
* Code: 401 UNAUTHORIZED
* Content: `{ detail : "Authentication credentials were not provided." }`
* Reason: Authentication credentials were not provided.

### Invalid Token
* Code: 401 UNAUTHORIZED
* Content: `{ detail : "Invalid Token." }`
* Reason: Invalid OAuth Token.

## Course Completions

This endpoint provides information about users that have completed a course. Can be called with filters for finding courses completed during a specified time period, or can be called without parameters in order to get information for all course completions.

* URL: `api/course_completion/v0/batch`
* Method: `GET`
* Optional URL Params:
	* `updated_before` (YYYY-MM-DDTHH:MM:SSZ) 
	* `updated_after` (YYYY-MM-DDTHH:MM:SSZ) 

* Success Response
	* Code: 200
	* Content:
	```
[
 {
 "email”: "alice@example.com”,
 "course_name”: "Control of Substances Hazardous to Health (CoSHH)”,
 "course_id”: "course-v1:ExtraCareCharitableTrust+CoSHH-2016+A”,
 "grade”: 0.9,
 "completion_date”: "2016-01-01 23:59:59”
 },
 {
 "email”: "bob@example.com”,
 "course_name”: "Control of Substances Hazardous to Health (CoSHH)”,
 "course_id”: "course-v1:ExtraCareCharitableTrust+CoSHH-2016+A”,
 "grade”: 1.0,
 "completion_date”: "2016-01-09 11:00:44”
 },
  ...
]
 	```
* 	Example calls:
	* `/api/course_completion/v0/batch` All data on all course completions
	* `/api/course_completion/v0/batch?updated_after=2015-12-09T00:00:00Z` Get data on courses completed after Dec 9th 2015
	* `/api/course_completion/v0/batch?updated_after=2015-12-09T00:00:00Z&updated_before=2015-12-19T00:00:00Z` Get data on courses completed between Dec 9th and 19th 2015

