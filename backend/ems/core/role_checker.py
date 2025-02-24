from functools import wraps
from django.http import JsonResponse
import jwt
from django.conf import settings


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Extract token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse(
                    {"error": "Unauthorized - Missing token"}, status=401
                )

            try:
                # Decode token
                token = auth_header.split(" ")[1]
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,  # Your Django secret key
                    algorithms=["HS256"],
                )

                # Get role from token payload
                user_role = payload.get("role")

                # Role validation
                if user_role not in allowed_roles:
                    return JsonResponse(
                        {"error": f"Forbidden - Requires {allowed_roles}"}, status=403
                    )

                # Attach role to request for later use
                request.user_role = user_role
                return view_func(request, *args, **kwargs)

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)

        return _wrapped_view

    return decorator
