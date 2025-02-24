from datetime import datetime, timedelta, timezone
from django.conf import settings
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def JWT_generator(**kwargs):
    """
    Generate a JWT (JSON Web Token).
    
    Args:
        **kwargs: Key-value pairs to be included in the token payload.
                 Example: username="Fady", role="admin"
    
    Returns:
        str: Generated JWT token.
        
    Raises:
        Exception: For unexpected errors during token generation.
    """

    if not kwargs:
        raise Exception("Empty payload")
    
    try:
        payload = {key: value for key, value in kwargs.items()}
        
        payload["exp"] = datetime.now(timezone.utc) + timedelta(days=7)
        payload["iat"] = datetime.now(timezone.utc) 

        token = jwt.encode(payload, settings.SECRET_KEY_JWT, algorithm="HS256")

        return token
    
    except Exception as e:
        raise Exception(f"Error generating JWT token: {str(e)}")
    

def validate_JWT(token):
    """
        Validate the JWT (JSON Web Token).
        
        Args:
            token: str.
        
        Returns:
            token's payload: dict containing the token's payload
            
        Raises:
            ExpiredSignatureError
            InvalidTokenError
    """
    try:
        if not token:
            raise Exception("No token provided")
    
        decoded_token = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=["HS256"])

        return decoded_token

    except ExpiredSignatureError as e:
        raise Exception("Token is expired")
    
    except InvalidTokenError as e:
        raise Exception("Invalid token")
