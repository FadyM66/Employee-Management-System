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
    
    