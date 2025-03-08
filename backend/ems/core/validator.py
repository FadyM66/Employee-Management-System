from django.core.exceptions import ValidationError
import re
from .responses import Responses as r

class validator:
    
    """

        Usage:
            for request's data validation.
        
        Instructions:
            name must be not less than 2 & not exceed 255.
            password must be strong:
                - One upper letter at least
                - One lower letter at least
                - One number at least 
                - One symbol at least
                - Min length is 8
            email must follow these:
                - total length not exceed 255
                - include @ and . e.g. python@yahoo.com
            status must be one of four (1, 2, 3, 4)
            role must be one of these [admin, user, manager]
            mobile phone must start with +02 or 0, then 1 + [0 or 1 or 2 or 5] + 8 digits
            address must be string

        Args:
            data: dictionary

        Returns:
            validated data

        Raises:
            validation error

    """
    
    # Fields specs

    fields_specs = {
        'name' : {'type': str, 'min': 2, 'max': 255, 'regx': r'^[A-Za-z\s]+$'},
        'company' : {'type': str, 'min': 2, 'max': 255, 'regx': r'^[A-Za-z\s]+$'},
        'password' : {'type': str, 'min': 8, 'regx': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'},
        'email' : {'type': str, 'regx': r'^(?=.{1,255}$)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'},
        'status': {'type': str, 'options': ['Application Received', 'Interview Scheduled', 'Not Accepted', 'Hired']},
        'mobile_phone': {'type': str, 'regx': r'^(?:\+20|0)1[0125]\d{8}$'},
        'address': {'type': str},
        'role': {'type': str, 'options': ['admin', 'manager', 'employee']}
    }

    # General validator

    @staticmethod
    def validator(data: dict):
        validated_data = {}
        errors = {}
        
        for field, value in data.items():
            if field in validator.fields_specs:
                field_spec = validator.fields_specs[field]
                
                # Type validation
                if not isinstance(value, field_spec['type']):
                    errors[field] = f"Must be {field_spec['type'].__name__}"
                    continue
                
                # Length validation
                if 'min' in field_spec and len(value) < field_spec['min']:
                    errors[field] = f"Must be at least {field_spec['min']} characters"
                    continue
                
                if 'max' in field_spec and len(value) > field_spec['max']:
                    errors[field] = f"Must not exceed {field_spec['max']} characters"
                    continue
                
                # Regex validation
                if 'regx' in field_spec:
                    if not re.fullmatch(field_spec['regx'], value):
                        errors[field] = f"Invalid {field} format"
                        continue
                
                # Options validation
                if 'options' in field_spec and value not in field_spec['options']:
                    errors[field] = f"Must be one of: {', '.join(field_spec['options'])}"
                    continue
                
                validated_data[field] = value
            else:
                errors[field] = "Invalid field"
        
        return validated_data if not errors else r.set_data(errors).invalid_data

    @staticmethod
    def email_validator(email):
        errors = {}
        if not isinstance(email, validator.fields_specs['email']['type']):
            errors['email'] = f"Must be {validator.fields_specs['email']['type'].__name__}"
        else:
            if not re.fullmatch(validator.fields_specs['email']['regx'], email):
                errors['email'] = "Invalid email format"
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def name_validator(name):
        errors = {}
        specs = validator.fields_specs['name']
        
        if not isinstance(name, specs['type']):
            errors['name'] = f"Must be {specs['type'].__name__}"
        elif len(name) < specs['min']:
            errors['name'] = f"Must be at least {specs['min']} characters"
        elif len(name) > specs['max']:
            errors['name'] = f"Must not exceed {specs['max']} characters"
        elif not re.fullmatch(specs['regx'], name):
            errors['name'] = "name must contain only letters"
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def password_validator(password):
        errors = {}
        specs = validator.fields_specs['password']
        
        if not isinstance(password, specs['type']):
            errors['password'] = f"Must be {specs['type'].__name__}"
        elif len(password) < specs['min']:
            errors['password'] = f"Must be at least {specs['min']} characters"
        elif not re.fullmatch(specs['regx'], password):
            errors['password'] = "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def status_validator(status):
        errors = {}
        specs = validator.fields_specs['status']
        
        if not isinstance(status, specs['type']):
            errors['status'] = f"Must be {specs['type'].__name__}"
        elif status not in specs['options']:
            errors['status'] = f"Must be one of: {', '.join(specs['options'])}"
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def mobile_phone_validator(mobile_phone):
        errors = {}
        specs = validator.fields_specs['mobile_phone']
        
        if not isinstance(mobile_phone, specs['type']):
            errors['mobile_phone'] = f"Must be {specs['type'].__name__}"
        elif not re.match(specs['regx'], mobile_phone):
            errors['mobile_phone'] = "Invalid phone number format"
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def address_validator(address):
        errors = {}
        specs = validator.fields_specs['address']
        
        if not isinstance(address, specs['type']):
            errors['address'] = f"Must be {specs['type'].__name__}"
        elif len(address) < specs['min']:
            errors['address'] = f"Must be at least {specs['min']} characters"
        elif len(address) > specs['max']:
            errors['address'] = f"Must not exceed {specs['max']} characters"
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def role_validator(role):
        errors = {}
        specs = validator.fields_specs['role']
        
        if not isinstance(role, specs['type']):
            errors['role'] = f"Must be {specs['type'].__name__}"
        elif role not in specs['options']:
            errors['role'] = f"Must be one of: {', '.join(specs['options'])}"
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def validate_employee_signup(data: dict):
        required_fields = ['name', 'email', 'status', 'address', 'mobile_phone']
        errors = {}
        
        # Check for missing required fields
        for field in required_fields:
            if field not in data:
                errors[field] = "This field is required"
        
        if errors:
            return {'errors': errors}
            
        # Validate each field
        name_validation = validator.name_validator(data['name'])
        email_validation = validator.email_validator(data['email'])
        status_validation = validator.status_validator(data['status'])
        address_validation = validator.address_validator(data['address'])
        mobile_validation = validator.mobile_phone_validator(data['mobile_phone'])
        
        # Collect any validation errors
        for validation in [name_validation, email_validation, status_validation, 
                         address_validation, mobile_validation]:
            if isinstance(validation, dict) and 'errors' in validation:
                errors.update(validation['errors'])
        
        return True if not errors else {'errors': errors}

    @staticmethod
    def validate_user_signup(data: dict):
        if not data:
            return r.set_data(data=data).missing_data
        
        required_fields = ['name','email', 'password', 'role']
        validated_data = {}
        errors = {}
        
        # Check for missing required fields
        for field in required_fields:
            if field not in data:
                errors[field] = "Required"
        
        if errors:
            return r.set_data(errors).missing_data
            
        # Validate each field
        email_validation = validator.email_validator(data['email'])
        name_validation = validator.name_validator(data['name'])
        password_validation = validator.password_validator(data['password'])
        role_validation = validator.role_validator(data['role'])
        
        # Collect any validation errors
        for validation in [email_validation, name_validation, password_validation, role_validation]:
            if isinstance(validation, dict) and 'errors' in validation:
                errors.update(validation['errors'])
        
        if not errors:
            for field in required_fields:
                validated_data[field] = data[field]
        
        return (r.created, validated_data) if not errors else r.set_data(errors).invalid_data

    @staticmethod
    def validate_company_signup(data: dict):
        if 'name' not in data:
            return r.set_data({'errors': {'name': "This field is required"}}).missing_data
            
        is_valid = validator.name_validator(data['name'])
        
        return (r.created, {"name": data['name']}) if is_valid == True else r.set_data(is_valid).invalid_data
                 

    @staticmethod
    def validate_department_signup(data: dict):
        if 'name' not in data.keys():
            return r.set_data({'errors': {'name': "This field is required"}}).missing_data
        
        if 'company' not in data.keys():
            return r.set_data({'errors': {'company': "This field is required"}}).missing_data

        name_validation = validator.name_validator(data['name'])
        company_validation = validator.name_validator(data['company'])
        
        if name_validation == True and company_validation == True:
            return (r.created, {"name": data['name'], 'company': data['company']})
        
        errors = {}
        
        if name_validation != True and 'errors' in name_validation and 'name' in name_validation['errors']:
            errors['name'] = name_validation['errors']['name']
        
        if company_validation != True and 'errors' in company_validation and 'name' in company_validation['errors']:
            errors['company'] = company_validation['errors']['name']
        
        return r.set_data({'errors': errors}).invalid_data            