from django.core.exceptions import ObjectDoesNotExist

from openedx.core.lib.api.view_utils import add_serializer_errors

from openedx.core.djangoapps.user_api.errors import (
    AccountUpdateError, AccountValidationError, 
    UserAPIInternalError, UserAPIRequestError, UserNotFound, UserNotAuthorized
)
from openedx.core.djangoapps.user_api.helpers import intercept_errors
from django.contrib.auth.models import User

from .models import StudentStudyLocation, StudyLocation
from .serializers import StudentStudyLocationSerializer


# @intercept_errors(UserAPIInternalError, ignore_errors=[UserAPIRequestError])
def get_student_studylocation(requesting_user, username=None):
    """
    Returns Study Location information for a user serialized as JSON.

    Note:
        If `requesting_user.username` != `username`, this method will return differing amounts of information
        based on who `requesting_user` is and the privacy settings of the user associated with `username`.

    Args:
        requesting_user (User): The user requesting the account information. Only the user with username
            `username` or users with "is_staff" privileges can get full account information.
            Other users will get the account fields that the user has elected to share.
        username (str): Optional username for the desired account information. If not specified,
            `requesting_user.username` is assumed.

    Returns:
         A dict containing account fields.

    Raises:
         UserNotFound: no user with username `username` exists (or `requesting_user.username` if
            `username` is not specified)
         UserAPIInternalError: the operation failed due to an unexpected error.
    """

    if username is None:
        username = requesting_user.username

    has_full_access = requesting_user.username == username or requesting_user.is_staff

    if not has_full_access:
        return {}

    student = User.objects.get(username=username)
    student_studylocation = StudentStudyLocation.location_for_student(student)
    serializer = StudentStudyLocationSerializer(student_studylocation)
    
    serialized = dict(**serializer.data)
    return serialized


@intercept_errors(UserAPIInternalError, ignore_errors=[UserAPIRequestError])
def add_student_studylocation(requesting_user, update, username=None):
    """Update Student Study Location information.  An update adds rather than
    modifies.

    Note:
        It is up to the caller of this method to enforce the contract that this method is only called
        with the user who made the request.

    Arguments:
        requesting_user (User): The user requesting to modify account information. Only the user with username
            'username' has permissions to modify account information.
        update (dict): The updated account field values.
        username (str): Optional username specifying which account should be updated. If not specified,
            `requesting_user.username` is assumed.

    Raises:
        UserNotFound: no user with username `username` exists (or `requesting_user.username` if
            `username` is not specified)
        UserNotAuthorized: the requesting_user does not have access to change the account
            associated with `username`
        AccountValidationError: the update was not attempted because validation errors were found with
            the supplied update
        AccountUpdateError: the update could not be completed. Note that if multiple fields are updated at the same
            time, some parts of the update may have been successful, even if an AccountUpdateError is returned.
        UserAPIInternalError: the operation failed due to an unexpected error.
    """

    if username is None:
        username = requesting_user.username

    if requesting_user.username != username:
        raise UserNotAuthorized()

    # Build up all field errors, whether read-only, validation, or email errors.
    field_errors = {}

    student = User.objects.get(username=username)
    update['user'] = student.id
    serializer = StudentStudyLocationSerializer(data=update)
    field_errors = add_serializer_errors(serializer, update, field_errors)

    # If we have encountered any validation errors, return them to the user.
    if field_errors:
        raise AccountValidationError(field_errors)

    try:
        # If everything validated, go ahead and save the serializers.
        serializer.save()

    except Exception as err:
        raise AccountUpdateError(
            u"Error thrown when saving Student Location updates: '{}'".format(err.message)
        )
