# Enviornment Notes

On devstack, there appears to be a race condition in loading the apps where course_access_group does not load into the admin interface when course_access_group is added to `INSTALLED_APPS` in aws.py. 


# Overview

This file provides additional information on the LMS environment.


# Taxoman on Devstack

_TODO: Update the Taxoman Dogwood devstack instructions in openedx-docs and link here_

In devstack, when LMS is run with paver, packages specified in the lms/requirements/ files will override any custom package installs. This impacts devstack configurations of Taxoman integrations because edx-search is a custom branch. 

Therefore, if you are developing/customizing edx-search, then disable the edx-search line in requirements/edx/github.txt

If you don't see `course_access_group` as an option in `/admin/` then do the following:

remove or remark out `INSTALLED_APPS += ('course_access_group',)` in `lms/envs/aws.py` and add `'course_access_group'` to the `INSTALLED_APPS in `lms/envs/common.py`

This *should* address a race condition in admin initializing before `couese_access_group` has initialized.


