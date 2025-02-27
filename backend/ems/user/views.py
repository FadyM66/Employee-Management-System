from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from core.validator import validator
from .models import User
from .serializer import user_serializer
from core.responses import Responses as r
from core.utils import hash_password
from .models import User
from .utils import login_utility
from core.role_checker import role_required
from core.role_permitter import role_permitter


@api_view(['POST'])
@role_required(['admin', 'manager'])
@role_permitter
def register(request):
    try:
        """ Register endpoint """
        new_user_data = request.data
        
        # Validate the incoming data      
        response, validated_data  = validator.validate_user_signup(new_user_data)
        
        # Create new user
        if validated_data:
            
            # Replace the plain password with hashed one
            validated_data['password'] = hash_password(validated_data['password'])
            new_user = User(**validated_data)
            new_user.save()
            
            return response
        
        else:
            return response
    
    except IntegrityError as e:
        return r.set_data({}).conflict
        
    except Exception as e:
        return r.set_data({}).server_error
    
    
@api_view(['POST'])
def login(request):
    try:
        """ Login endpoint"""
        login_data = request.data
        
        # Login using login_utility
        response = login_utility(login_data)
        
        return response
    
    except Exception as e:
        return r.server_error
    
    
