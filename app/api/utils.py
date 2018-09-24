from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied


def get_pagination_params(request):
    try:
        try:
            offset = int(request.GET.get('offset'))
        except TypeError:
            offset = 0

        try:
            limit = int(request.GET.get('limit'))
        except TypeError:
            limit = None

        if offset is None:
            offset = 0
        if limit is None:
            pass

        if offset < 0 or (limit is not None and limit < 0):
            raise PaginationParamsError
    except (ValueError, AssertionError):
        raise PaginationParamsError

    return offset, limit


def authenticate_user(username, password):
    try:
        u = authenticate(username=username, password=password)
    except PermissionDenied:
        raise UserError('Permission denied.')

    if u is None:
        raise UserError('User not found.')

    return u


class PaginationParamsError(Exception):
    """Exception raised for errors in the input."""

    def __init__(self):
        self.json_response = JsonResponse({
            'status': 'ERROR',
            'message': 'Bad pagination parameters.'
        })


class UserError(Exception):
    """Exception raised for errors in the user authentication."""

    def __init__(self, message):
        self.json_response = JsonResponse({
            'status': 'ERROR',
            'message': message
        })
