from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException,
    _get_error_details,
    ValidationError as DRFValidationError,
)


class ValidationErrorData:
    """
    Class that enables to return multiple errors, each with specific code, when raising
    CustomValidationError. This class comes into use in the _get_error_details method of the
    APIException class.
    """

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):  # noqa pylint: disable=W0231
        if detail is None:
            detail = self.default_detail
        elif isinstance(detail, ValidationError):
            detail = [
                ValidationErrorData(item.messages[0], item.code.upper())
                for item in detail.error_list
            ]
        if code is None:
            code = self.default_code

        if isinstance(detail, list):
            self.detail = _get_error_details(detail, code)
        else:
            self.detail = [_get_error_details(detail, code)]


def _get_non_field_errors_or_none(full_details):
    if isinstance(full_details, dict):
        for key in ["non_field_errors", NON_FIELD_ERRORS]:
            non_field_errors = full_details.get(key)
            if non_field_errors:
                return non_field_errors
    return None


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = DRFValidationError(detail=exc.message_dict)

    response = exception_handler(exc, context)
    if response is not None:
        try:
            full_details = exc.get_full_details()
        except AttributeError:
            return response
        non_field_errors = _get_non_field_errors_or_none(full_details)
        if non_field_errors:
            for item in non_field_errors:
                item["code"] = item["code"].upper()
            response.data = non_field_errors
        else:
            response.data = full_details
    return response
