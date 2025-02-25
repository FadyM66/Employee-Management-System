from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.validator import validator
from .models import User
from .serializer import user_serializer
from core.responses import Responses as r


@api_view(['POST'])
def register(request):

    new_user_data = request.data
    
    is_valid = validator.validate_user_signup(new_user_data)
    
    if is_valid:
        # return r.set_data(new_user_data).created
        return is_valid
    else:
        return r.server_error