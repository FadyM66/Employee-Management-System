from rest_framework.decorators import api_view
from django.db import IntegrityError
from core.validator import validator
from .serializer import user_serializer
from core.responses import Responses as r
from core.utils import hash_password
from .models import User
from .utils import login_utility
from core.role_checker import role_required
from core.role_permitter import role_permitter


@api_view(["POST"])
@role_required(["admin", "manager"])
@role_permitter
def register(request):
    """Register endpoint"""

    try:
        # Validate the incoming data
        result = validator.validate_user_signup(request.data)

        if isinstance(result, tuple):
            response, validated_data = result

            if validated_data:
                # Create new user
                # Replace the plain password with hashed one
                validated_data["password"] = hash_password(validated_data["password"])
                new_user = request.model(**validated_data)
                new_user.save()
                return response

        return result

    except IntegrityError as e:
        return r.set_data({str(e)}).invalid_data

    except Exception as e:
        return r.set_data({}).server_error


@api_view(["POST"])
def login(request):
    """Login endpoint"""

    try:

        login_data = request.data

        # Login using login_utility
        response = login_utility(login_data)

        return response

    except Exception as e:
        return r.server_error


@api_view(["GET"])
@role_required(["admin", "manager", "user"])
@role_permitter
def get_user(request):
    """Get user data endpoint"""

    try:

        if request.records:

            data = user_serializer(request.records, many=True).data
            return r.set_data(data).ok

        else:
            return r.not_found

    except Exception as e:
        return r.server_error


@api_view(["DELETE"])
@role_required(["admin", "manager"])
@role_permitter
def delete_user(request):
    """Delete user endpoint"""

    try:

        if request.records:
            request.records.delete()
            return r.ok

        else:
            return r.not_found

    except Exception as e:
        return r.server_error
