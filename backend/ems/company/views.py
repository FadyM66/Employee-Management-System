from rest_framework.decorators import api_view
from core.role_checker import role_required
from core.role_permitter import role_permitter
from core.validator import validator
from core.responses import Responses as r
from django.db import IntegrityError
from .serializer import company_serializer


@api_view(['POST'])
@role_required(['admin'])
@role_permitter
def create(request):
    """Create company endpoint"""
    try:
        new_record_data = request.data
        result = validator.validate_company_signup(new_record_data)
        model = request.model
        
        if isinstance(result, tuple):
            response, validated_data = result
            
            new_company = model(**validated_data)
            new_company.save()
            return response
        
        else:
            return result
    
    except IntegrityError as e:
        print(f"Error: {str(e)}")
        return r.conflict

    except Exception as e :
        print(f'Error: {str(e)}')
        return r.server_error
    
    
@api_view(['GET'])
@role_required(['admin', 'manager'])
@role_permitter
def get(request):
    """Get company endpoint"""
    try:
        records = request.records
        serialized_records = company_serializer(records, many=True).data

        return r.set_data(serialized_records).ok

    except Exception as e :
        print(f'Error: {str(e)}')
        return r.server_error
    

@api_view(['DELETE'])
@role_required(['admin'])
@role_permitter
def delete(request):
    """Delete company endpoint"""

    try:

        if request.records:
            request.records.delete()
            return r.ok

        else:
            return r.not_found

    except Exception as e:
        return r.server_error


@api_view(['PATCH'])
@role_required(['admin'])
@role_permitter
def update(request):
    """Update company endpoint"""
    
    try:
        company_name = request.data['name']
        model = request.model
        company = model.objects.filter(name=company_name).first()
        
        if not company:
            return r.not_found
        
        new_record_data = request.data['new_data']
        result = validator.validator(new_record_data)
        if isinstance(result, dict):  
            for key, value in result.items():
                setattr(company, key, value)         
            company.save()
            return r.ok
        else:
            return r.invalid_data
            
    except IntegrityError as e:
        print(f"Error: {str(e)}")
        return r.conflict

    except Exception as e :
        print(f'Error: {str(e)}')
        return r.server_error