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
    
    """ Register endpoint """
    
    try:
        new_user_data = request.data
        
        # Validate the incoming data      
        result = validator.validate_user_signup(new_user_data)
        
        if isinstance(result, tuple):
            response, validated_data = result

            if validated_data:
                # Create new user
                # Replace the plain password with hashed one
                validated_data['password'] = hash_password(validated_data['password'])
                new_user = User(**validated_data)
                new_user.save()
                return response        
        
        return result
    
    except IntegrityError as e:
        return r.set_data({}).conflict
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return r.set_data({}).server_error
    
    
@api_view(['POST'])
def login(request):

    """ Login endpoint """

    try:
        login_data = request.data
        
        # Login using login_utility
        response = login_utility(login_data)
        
        return response
    
    except Exception as e:
        return r.server_error
    

# @api_view(['GET'])
# @role_required(['admin', 'manager', 'user'])
# @role_permitter
# def get_user(request):
    
#     """ Get user data endpoint """

#     try:
#         payload = request.payload
        
#         if payload.get('email') and hasattr(request, 'data_query'):
#             data_query = request.data_query
#             user_data = data_query.filter(email=payload.get('email'))
#             serialized_data = user_serializer(user_data)
#             return r.set_data(serialized_data).ok
        
#         if payload.get('role') == 'admin':
#             user_data = User.objects.get(email=payload.get('role'))
        
#     except:
#         ...
        
        

@api_view(['DELETE'])
@role_required(['admin', 'manager'])
@role_permitter
def delete_user(request):
    
    """ Delete user endpoint """

    try:
       # Get email of user to delete
        to_delete_email = request.data.get('email')
        
        if not to_delete_email:
            return r.missing_data

       # Find the user to delete
        try:
            user_to_delete = User.objects.get(email=to_delete_email)
        except User.DoesNotExist:
            return r.not_found

       # Check manager permissions (admins already have full access from decorators)
        role = request.payload.get('role')
        
        if role == 'manager':
            manager = request.data_query 
            if user_to_delete.department != manager:
                return r.forbidden
        
        # Delete the user
        user_to_delete.delete()
        
        return r.set_data({"email": to_delete_email}).ok
                
    except Exception as e:
        return r.set_data({"detail": str(e)}).server_error
    
    
@api_view(['PATCH'])
@role_required(['admin', 'manager'])
@role_permitter
def update_user(request):
   
   """ Update user endpoint """

   try:
       # Get email of user to update
       to_update_email = request.data.get('email')
       update_data = request.data.get('update_data')
       
       if not to_update_email or not update_data:
           return r.missing_data
       
       # Find the user to update
       try:
           user_to_update = User.objects.get(email=to_update_email)
       except User.DoesNotExist:
           return r.not_found
       
       # Check manager permissions
       role = request.payload.get('role')
       if role == 'manager':
           manager_department = request.data_query
           if user_to_update.department != manager_department or 'role' in update_data.keys():
               return r.forbidden
       
       # Update user fields
       for field, value in update_data.items():
           setattr(user_to_update, field, value)
       
       user_to_update.save()
       
       return r.set_data({"email": to_update_email}).ok
               
   except Exception as e:
       return r.set_data({"detail": str(e)}).server_error